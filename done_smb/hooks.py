# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from . import __version__ as app_version

app_name = "done_smb"
app_title = "Done Smb"
app_publisher = "smb"
app_description = "done"
app_icon = "octicon octicon-file-directory"
app_color = "grey"
app_email = "smb"
app_license = "MIT"

# Includes in <head>
# ------------------

# include js, css files in header of desk.html
# app_include_css = "/assets/done_smb/css/done_smb.css"
# app_include_js = "/assets/done_smb/js/done_smb.js"

# include js, css files in header of web template
# web_include_css = "/assets/done_smb/css/done_smb.css"
# web_include_js = "/assets/done_smb/js/done_smb.js"

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

# Website user home page (by function)
# get_website_user_home_page = "done_smb.utils.get_home_page"

# Generators
# ----------

# automatically create page for each record of this doctype
# website_generators = ["Web Page"]

# Installation
# ------------

# before_install = "done_smb.install.before_install"
# after_install = "done_smb.install.after_install"

# Desk Notifications
# ------------------
# See frappe.core.notifications.get_notification_config

# notification_config = "done_smb.notifications.get_notification_config"

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

# Document Events
# ---------------
# Hook on document methods and events

doc_events = {
	"Contract": {
		"validate": "done_smb.set_value_contract",
	},
	"Sales Invoice" :{
		"validate": "done_smb.set_warehouse_sales_invoice",

	}
}

# Scheduled Tasks
# ---------------

scheduler_events = {
# 	"all": [
# 		"done_smb.tasks.all"
# 	],
	"daily": [
		"done_smb.__init__.leave_allocate_annual",
        # "done_smb.__init__.leave_allocate_sick"
	]
# 	"hourly": [
# 		"done_smb.tasks.hourly"
# 	],
# 	"weekly": [
# 		"done_smb.tasks.weekly"
# 	]
# 	"monthly": [
# 		"done_smb.tasks.monthly"
# 	]
}

# Testing
# -------

# before_tests = "done_smb.install.before_tests"

# Overriding Methods
# ------------------------------
#
# override_whitelisted_methods = {
# 	"frappe.desk.doctype.event.event.get_events": "done_smb.event.get_events"
# }
#
# each overriding function accepts a `data` argument;
# generated from the base implementation of the doctype dashboard,
# along with any modifications made in other Frappe apps
# override_doctype_dashboards = {
# 	"Task": "done_smb.task.get_dashboard_data"
# }


jenv = {
	"methods":[
		"get_date:done_smb.get_date",
		"get_details:done_smb.get_details",
		"salary_detail:done_smb.salary_detail",
		"employee_detail_arabic:done_smb.employee_detail_arabic",
		"annual_leave_form:done_smb.annual_leave_form",
		"get_leave:erpnext.hr.doctype.leave_application.leave_application.get_leave_details",
		"get_allow:done_smb.get_allowence",
		"sick_leave:done_smb.get_sick_leave",
		"indemnity:done_smb.custom.calculate_indemnity",
		"error:done_smb.throw_msg",
		"total_salary:done_smb.salary_sum",
		"total_unpaid_days:done_smb.unpaid_days_sum"
	]
}
