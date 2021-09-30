from . import __version__ as app_version

app_name = "ecs_tax_invoices"
app_title = "ECS Tax Invoices"
app_publisher = "ERP Cloud Systems"
app_description = "Custom App For Tax Invoices"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "info@erpcloud.systems"
app_license = "MIT"

# Includes in <head>
# ------------------
doc_events = {
"Sales Order": {
	"validate": "ecs_tax_invoices.ecs_tax_invoices.overrides.sales_order.sales_order.validate_tax_type"
},
"Sales Invoice": {
	"validate": "ecs_tax_invoices.ecs_tax_invoices.overrides.sales_invoice.sales_invoice.validate_tax_type"
}
}
doctype_js = {
	"Sales Order": "ecs_tax_invoices/overrides/sales_order/sales_order.js",
    "Sales Invoice": "ecs_tax_invoices/overrides/sales_invoice/sales_invoice.js"
}

# include js, css files in header of desk.html
# app_include_css = "/assets/ecs_tax_invoices/css/ecs_tax_invoices.css"
# app_include_js = "/assets/ecs_tax_invoices/js/ecs_tax_invoices.js"

# include js, css files in header of web template
# web_include_css = "/assets/ecs_tax_invoices/css/ecs_tax_invoices.css"
# web_include_js = "/assets/ecs_tax_invoices/js/ecs_tax_invoices.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "ecs_tax_invoices/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
#	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "ecs_tax_invoices.install.before_install"
# after_install = "ecs_tax_invoices.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "ecs_tax_invoices.notifications.get_notification_config"

# Permissions
# -----------
# Permissions evaluated in scripted ways

# permission_query_conditions = {
# 	"Event": "frappe.desk.doctype.event.event.get_permission_query_conditions",
# }
#
# has_permission = {
# 	"Event": "frappe.desk.doctype.event.event.has_permission",
# }

# DocType Class
# ---------------
# Override standard doctype classes

# override_doctype_class = {
# 	"ToDo": "custom_app.overrides.CustomToDo"
# }

# Document Events
# ---------------
# Hook on document methods and events

# doc_events = {
# 	"*": {
# 		"on_update": "method",
# 		"on_cancel": "method",
# 		"on_trash": "method"
#	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"ecs_tax_invoices.tasks.all"
# 	],
# 	"daily": [
# 		"ecs_tax_invoices.tasks.daily"
# 	],
# 	"hourly": [
# 		"ecs_tax_invoices.tasks.hourly"
# 	],
# 	"weekly": [
# 		"ecs_tax_invoices.tasks.weekly"
# 	]
# 	"monthly": [
# 		"ecs_tax_invoices.tasks.monthly"
# 	]
# }

# Testing
# -------

# before_tests = "ecs_tax_invoices.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "ecs_tax_invoices.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "ecs_tax_invoices.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]


# User Data Protection
# --------------------

user_data_fields = [
	{
		"doctype": "{doctype_1}",
		"filter_by": "{filter_by}",
		"redact_fields": ["{field_1}", "{field_2}"],
		"partial": 1,
	},
	{
		"doctype": "{doctype_2}",
		"filter_by": "{filter_by}",
		"partial": 1,
	},
	{
		"doctype": "{doctype_3}",
		"strict": False,
	},
	{
		"doctype": "{doctype_4}"
	}
]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"ecs_tax_invoices.auth.validate"
# ]

