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
            item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """, group, as_dict=1)
            for z in item_taxes_template:
                y.item_tax_template = z.item_tax_template
        for x in doc.taxes:
            x.included_in_print_rate = 1
    if doc.tax_type == "Excluded":
        for y in doc.items:
            group = y.item_group
            item_taxes_template = frappe.db.sql(""" select item_tax_template from `tabItem Tax` where parent=%s """, group, as_dict=1)
            for z in item_taxes_template:
                y.item_tax_template = z.item_tax_template
        for x in doc.taxes:
            x.included_in_print_rate = 0
    if doc.tax_type == "Commercial":
        for x in doc.items:
            x.item_tax_template = ""
        doc.set("taxes", [])