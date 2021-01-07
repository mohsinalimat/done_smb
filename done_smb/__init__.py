# -*- coding: utf-8 -*-
from __future__ import unicode_literals

__version__ = '0.0.1'
import frappe

def leave_allocate_annual():
		import datetime 
		import calendar
		import math
		from datetime import date, timedelta
		today = date.today()
		first_date = today.replace(day = 7)
		if first_date == today:
			today_list = (today.strftime("%d-%m-%Y")).split("-")
			employees =  frappe.db.sql("""select name, employee_name from `tabEmployee` where status = "Active" """,as_dict = 1)
			for employee in employees:
				leave_alloc_doc = frappe.new_doc("Leave Allocation")
				leave_alloc_doc.employee = employee["name"]
				leave_alloc_doc.employee_name = employee["employee_name"]
				leave_alloc_doc.leave_type =  'Annual leave'
				leave_alloc_doc.from_date = today
				last_date = calendar.monthrange(int(today_list[2]),int(today_list[1]))[1]
				leave_alloc_doc.to_date = datetime.date(int(today_list[2]), int(today_list[1]), int(last_date))
				if frappe.db.exists("Leave Allocation",{"employee":employee.name,"leave_type":"Annual Leave"}):
						leave_alloc_doc.new_leaves_allocated = 2.5
						leave_alloc_doc.carry_forward = 1
				else:
						leave_alloc_doc.new_leaves_allocated = 2.5
						# joining_date =  frappe.db.sql("select date_of_joining from `tabEmployee` where name =%s",(employee["name"]),as_dict =1)
						# leave_alloc_doc.new_leaves_allocated = math.floor(((today - joining_date[0]["date_of_joining"]).days)*(2.5/30))
				leave_alloc_doc.save()
				leave_alloc_doc.submit()


def leave_allocate_sick():
	import datetime 
	import calendar
	import math
	from datetime import date, timedelta
	leave_types = ["25 Percent unpaid Sick", "50 Percent unpaid Sick", "75 Percent unpaid Sick", "Sick Leave Unpaid", "Sick Leave"]
	today = date.today()
	first_date = today.replace(day=1,month=1)
	if first_date == today:
		today_list = (today.strftime("%d-%m-%Y")).split("-")
		employees =  frappe.db.sql("""select name, employee_name from `tabEmployee` where status = "Active" """,as_dict = 1)
		for employee in employees:
			for leave_type in leave_types:			
				leave_alloc_doc = frappe.new_doc("Leave Allocation")
				leave_alloc_doc.employee = employee["name"]
				leave_alloc_doc.employee_name = employee["employee_name"]
				leave_alloc_doc.leave_type =  leave_type
				leave_alloc_doc.from_date = today
				leave_alloc_doc.to_date =  today.replace(day=31,month=12)
				leave_alloc_doc.new_leaves_allocated = 6
				leave_alloc_doc.save()
				leave_alloc_doc.submit()
