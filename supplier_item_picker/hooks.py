app_name = "supplier_item_picker"
app_title = "Supplier Item Picker"
app_publisher = "Ameer Muavia Shah"
app_description = "Helps you add multiple items from a selected supplier"
app_email = "mavee.shah@hotmail.com"
app_license = "mit"
# required_apps = []

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/supplier_item_picker/css/supplier_item_picker.css"
# app_include_js = "/assets/supplier_item_picker/js/supplier_item_picker.js"

# include js, css files in header of web template
# web_include_css = "/assets/supplier_item_picker/css/supplier_item_picker.css"
# web_include_js = "/assets/supplier_item_picker/js/supplier_item_picker.js"

# include custom scss in every website theme (without file extension ".scss")
# website_theme_scss = "supplier_item_picker/public/scss/website"

# include js, css files in header of web form
# webform_include_js = {"doctype": "public/js/doctype.js"}
# webform_include_css = {"doctype": "public/css/doctype.css"}

# include js in page
# page_js = {"page" : "public/js/file.js"}

# include js in doctype views
# doctype_js = {"doctype" : "public/js/doctype.js"}
doctype_js = {"Purchase Order" : "public/js/purchase_order.js"}
# doctype_list_js = {"doctype" : "public/js/doctype_list.js"}
# doctype_tree_js = {"doctype" : "public/js/doctype_tree.js"}
# doctype_calendar_js = {"doctype" : "public/js/doctype_calendar.js"}

# Svg Icons
# ------------------
# include app icons in desk
# app_include_icons = "supplier_item_picker/public/icons.svg"

# Home Pages
# ----------

# application home page (will override Website Settings)
# home_page = "login"

# website user home page (by Role)
# role_home_page = {
# 	"Role": "home_page"
# }

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Jinja
# ----------

# add methods and filters to jinja environment
# jinja = {
# 	"methods": "supplier_item_picker.utils.jinja_methods",
# 	"filters": "supplier_item_picker.utils.jinja_filters"
# }

# Installation
# ------------

# before_install = "supplier_item_picker.install.before_install"
# after_install = "supplier_item_picker.install.after_install"

# Uninstallation
# ------------

# before_uninstall = "supplier_item_picker.uninstall.before_uninstall"
# after_uninstall = "supplier_item_picker.uninstall.after_uninstall"

# Integration Setup
# ------------------
# To set up dependencies/integrations with other apps
# Name of the app being installed is passed as an argument

# before_app_install = "supplier_item_picker.utils.before_app_install"
# after_app_install = "supplier_item_picker.utils.after_app_install"

# Integration Cleanup
# -------------------
# To clean up dependencies/integrations with other apps
# Name of the app being uninstalled is passed as an argument

# before_app_uninstall = "supplier_item_picker.utils.before_app_uninstall"
# after_app_uninstall = "supplier_item_picker.utils.after_app_uninstall"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "supplier_item_picker.notifications.get_notification_config"

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
# 	}
# }

# Scheduled Tasks
# ---------------

# scheduler_events = {
# 	"all": [
# 		"supplier_item_picker.tasks.all"
# 	],
# 	"daily": [
# 		"supplier_item_picker.tasks.daily"
# 	],
# 	"hourly": [
# 		"supplier_item_picker.tasks.hourly"
# 	],
# 	"weekly": [
# 		"supplier_item_picker.tasks.weekly"
# 	],
# 	"monthly": [
# 		"supplier_item_picker.tasks.monthly"
# 	],
# }

# Testing
# -------

# before_tests = "supplier_item_picker.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "supplier_item_picker.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "supplier_item_picker.task.get_dashboard_data"
# }

# exempt linked doctypes from being automatically cancelled
#
# auto_cancel_exempted_doctypes = ["Auto Repeat"]

# Ignore links to specified DocTypes when deleting documents
# -----------------------------------------------------------

# ignore_links_on_delete = ["Communication", "ToDo"]

# Request Events
# ----------------
# before_request = ["supplier_item_picker.utils.before_request"]
# after_request = ["supplier_item_picker.utils.after_request"]

# Job Events
# ----------
# before_job = ["supplier_item_picker.utils.before_job"]
# after_job = ["supplier_item_picker.utils.after_job"]

# User Data Protection
# --------------------

# user_data_fields = [
# 	{
# 		"doctype": "{doctype_1}",
# 		"filter_by": "{filter_by}",
# 		"redact_fields": ["{field_1}", "{field_2}"],
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_2}",
# 		"filter_by": "{filter_by}",
# 		"partial": 1,
# 	},
# 	{
# 		"doctype": "{doctype_3}",
# 		"strict": False,
# 	},
# 	{
# 		"doctype": "{doctype_4}"
# 	}
# ]

# Authentication and authorization
# --------------------------------

# auth_hooks = [
# 	"supplier_item_picker.auth.validate"
# ]

# Automatically update python controller files with type annotations for this app.
# export_python_type_annotations = True

# default_log_clearing_doctypes = {
# 	"Logging DocType Name": 30  # days to retain logs
# }

