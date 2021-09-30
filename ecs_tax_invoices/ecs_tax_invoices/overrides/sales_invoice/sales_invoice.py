# -*- coding: utf-8 -*-
# Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe, json
from frappe.model.document import Document
from frappe import _
from frappe.desk.search import sanitize_searchfield
from frappe.utils import (flt, getdate, get_url, now,
nowtime, get_time, today, get_datetime, add_days)
from frappe.utils import add_to_date, now, nowdate

@frappe.whitelist()
def validate_tax_type(doc, method=None):
    if doc.tax_type == "Included":
        for y in doc.items:
            group = y.item_group
            item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """,group,as_dict=1)
            for z in item_taxes_template:
                y.item_tax_template = z.item_tax_template
        for x in doc.taxes:
            x.included_in_print_rate = 1
    if doc.tax_type == "Excluded":
        for y in doc.items:
            group = y.item_group
            item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """,group,as_dict=1)
            for z in item_taxes_template:
                y.item_tax_template = z.item_tax_template
        for x in doc.taxes:
            x.included_in_print_rate = 0
    if doc.tax_type == "Commercial":
        for x in doc.items:
            x.item_tax_template = ""
        doc.set("taxes", [])

@frappe.whitelist()
def make_tax(doc, method=None):
    default_tax_acc = frappe.db.get_value("Company", doc.company, "default_taxes")
    deferred_tax_acc = frappe.db.get_value("Company", doc.company, "deferred_tax")
    default_income_account = frappe.db.get_value("Company", doc.company, "default_income_account")
    default_receivable_account = frappe.db.get_value("Company", doc.company, "default_receivable_account")
    #if doc.deferred_tax_jv:
    #	frappe.throw(_("لايمكن انشاء القيود مرة اخرى !"))
    if doc.tax_type in ("Included","Excluded"):
        accounts = [
            {
                "doctype": "Journal Entry Account",
                "account": default_tax_acc,
                "debit": 0,
                "credit": doc.total_taxes_and_charges,
                "credit_in_account_currency": doc.total_taxes_and_charges,
                "user_remark": doc.name
            },
            {
                "doctype": "Journal Entry Account",
                "account": deferred_tax_acc,
                "debit": doc.total_taxes_and_charges,
                "credit": 0,
                "debit_in_account_currency": doc.total_taxes_and_charges,
                "user_remark": doc.name
            }
        ]
        new_doc = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Deferred Revenue",
            "sales_invoice": doc.name,
            "company": doc.company,
            "posting_date": doc.posting_date,
            "accounts": accounts,
            "user_remark": _('ترحيل مخصص الضرائب  {0}').format(doc.name),
            "total_debit": doc.total_taxes_and_charges,
            "total_credit": doc.total_taxes_and_charges,
            "remark": _('ترحيل مخصص الضرائب  {0}').format(doc.name)

        })
        new_doc.insert()
        new_doc.submit()
        djv = new_doc.name
        docs = frappe.get_doc('Sales Invoice', doc.name)
        docs.deferred_tax_jv = djv
        docs.save()
        if not doc.serial:
            serial = frappe.get_doc({
                "doctype": "Invoice Serial",
                "link": doc.name,
                "status": "Active"
            })
            serial.insert()
            docs.serial = serial.name
        else:
            serial = frappe.get_doc('Invoice Serial', doc.serial)
            serial.status = "Active"
            serial.save()
            docs.serial = serial.name
        docs.save()

    elif doc.tax_type == "Commercial":
        #taxes_amount = float(doc.grand_total) - (float(doc.grand_total) / 1.14)
        grand_tax_amount = 0
        for y in doc.items:
            group = y.item_group
            item_taxes_template = frappe.db.get_value('Item Tax', {'parent': group}, ['item_tax_template'])
            item_taxes_rate = frappe.db.get_value('Item Tax Template Detail', {'parent': item_taxes_template}, ['tax_rate'])
            tax_rate = item_taxes_rate/100
            grand_tax_amount += tax_rate * y.amount

        accounts = [
            {
                "doctype": "Journal Entry Account",
                "account": default_tax_acc,
                "debit": 0,
                "credit": grand_tax_amount,
                "credit_in_account_currency": grand_tax_amount,
                "user_remark": doc.name
            },
            {
                "doctype": "Journal Entry Account",
                "account": default_receivable_account,
                "debit": grand_tax_amount,
                "party_type": "Customer",
                "party": doc.customer,
                "credit": 0,
                "debit_in_account_currency": grand_tax_amount,
                "user_remark": doc.name
            }
        ]
        new_doc = frappe.get_doc({
            "doctype": "Journal Entry",
            "voucher_type": "Deferred Revenue",
            "sales_invoice": doc.name,
            "company": doc.company,
            "posting_date": doc.posting_date,
            "accounts": accounts,
            "user_remark": _('ترحيل مخصص الضرائب  {0}').format(doc.name),
            "total_debit": grand_tax_amount,
            "total_credit": grand_tax_amount,
            "remark": _('ترحيل مخصص الضرائب  {0}').format(doc.name)

        })
        new_doc.insert()
        new_doc.submit()
        djv = new_doc.name
        docs = frappe.get_doc('Sales Invoice', doc.name)
        docs.deferred_tax_jv = djv

        if not doc.serial:
            serial = frappe.get_doc({
                "doctype": "Invoice Serial",
                "link": doc.name,
                "status": "Active"
            })
            serial.insert()
            docs.serial = serial.name
        else:
            serial = frappe.get_doc('Invoice Serial', doc.serial)
            serial.status = "Active"
            serial.save()
            docs.serial = serial.name
        docs.save()
    doc.reload()

@frappe.whitelist()
def cancel_tax(doc, method=None):
    inv = frappe.get_doc('Sales Invoice', doc.name)
    inv.deferred_tax_jv = ""
    jv = frappe.get_doc('Journal Entry', doc.deferred_tax_jv)
    jv.sales_invoice = ""
    serial = frappe.get_doc('Invoice Serial', doc.serial)
    serial.status = "Cancelled"
    inv.save()
    jv.save()
    serial.save()
    jv.cancel()
    delete = frappe.delete_doc("Invoice Serial", doc.serial)
    doc.serial = ""
    frappe.db.set_value("Sales Invoice", doc.name, "serial", "")
    frappe.db.commit()
    doc.reload()
    return delete