# Copyright (c) 2013, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, timedelta, datetime

def execute(filters=None):
	columns = [
		{
			"fieldname": "day",
			"fieldtype": "data",
			"label": "Day",
			"width": 0
		}, 
		{
			"fieldname": "date",
			"fieldtype": "date",
			"label": "Date",
			"width": 0	
		},
		{
			"fieldname": "time_in",
			"fieldtype": "time",
			"label": "Time IN",
			"width": 0,
		},
		{
			"fieldname": "time_out",
			"fieldtype": "time",
			"label": "Time OUT",
			"width": 0,
		}, 
		{
			"fieldname": "early_in",
			"fieldtype": "time",
			"label": "Early IN",
			"width": 0,
		},
		{
			"fieldname": "ealry_out",
			"fieldtype": "time",
			"label": "Early OUT",
			"width": 0,
		},
		{
			"fieldname": "late_in",
			"fieldtype": "time",
			"label": "Late IN",
			"width": 0,
		},
		{
			"fieldname": "late_out",
			"fieldtype": "time",
			"label": "Late OUT",
			"width": 0,
		},
		{
			"fieldname": "missing_in",
			"fieldtype": "data",
			"label": "Missing IN",
			"width": 0,
		},
		{
			"fieldname": "missing_out",
			"fieldtype": "data",
			"label": "Missing OUT",
			"width": 0,
		},
		{
			"fieldname": "permissions",
			"fieldtype": "data",
			"label": "Permissions",
			"width": 0,
		},
		{
			"fieldname": "official_duties",
			"fieldtype": "data",
			"label": "Official Duties",
			"width": 0,
		},
		{
			"fieldname": "attended_hours",
			"fieldtype": "time",
			"label": "Attended Hours",
			"width": 0,
		},
		{
			"fieldname": "working_hours",
			"fieldtype": "time",
			"label": "Working Hours",
			"width": 0,
		},
		{
			"fieldname": "annual_leave",
			"fieldtype": "data",
			"label": "Annual Leave",
			"width": 0,
		},
		{
			"fieldname": "sick_leave",
			"fieldtype": "data",
			"label": "Sick Leave",
			"width": 0,
		},
		{
			"fieldname": "other_leave",
			"fieldtype": "data",
			"label": "Other Leave",
			"width": 0,
		},
		{
			"fieldname": "official_duty",
			"fieldtype": "data",
			"label": "Official Duty",
			"width": 0,
		},
		{
			"fieldname": "training_course",
			"fieldtype": "data",
			"label": "Training course",
			"width": 0,
		},
		{	
			"fieldname": "business_trip",
			"fieldtype": "data",
			"label": "Business Trip",
			"width": 0,
		},
		{
			"fieldname": "absence",
			"fieldtype": "data",
			"label": "Absence",
			"width": 0,
		},
		{
			"fieldname": "avg_attendance",
			"fieldtype": "percent",
			"label": "Avg Attendance%",
			"precision": "2",
			"width": 0,
		},
		{
			"fieldname": "extra_hour_avg_attendance",
			"fieldtype": "percent",
			"label": "Extra Hours Avg Attendance%",
			"precision": "2",
			"width": 0,
		}
	]
	data = get_data(filters)
	return columns, data

def get_leave(emp_id, from_date, to_date, leave_type='Other Leave'):
	leave = ['Sick Leave Unpaid', '25 Percent unpaid Sick', '75 Percent unpaid Sick', '50 Percent unpaid Sick', 'Sick Leave']
	if leave_type == 'Sick Leave':
		dates = []
		for typ in leave:
			date = frappe.db.get_list("Leave Application", filters=[
					['status', '=', 'Approved'],
					['posting_date', '>=', from_date],
					['posting_date', '<=', to_date], 
					['employee', '=', emp_id],
					['leave_type', '=', typ]
				], fields=['from_date', 'to_date'])
			if len(date) != 0:
				date = get_leave_dates(date)
				for i in date:dates.append(i)
				return dates
		return 0
			
	filter = [
		["employee" ,"=", emp_id],
		["status", "=", "Approved"],
		["from_date", ">=", from_date],
		["from_date", "<=", to_date]]
	if leave_type == "Annual Leave":
		filter.append(["leave_type","=", leave_type])
	else:
		filter.append(["leave_type", "!=", "Annual Leave"])
		for leave_type in leave:
			filter.append(["leave_type", "!=", leave_type])
	leav_date = frappe.db.get_list("Leave Application", filters= filter, fields=['from_date', 'to_date'])
	if len(leav_date) != 0:
		return get_leave_dates(leav_date)
	return 0

def get_leave_dates(leave):
	leave_dates = []
	for i in leave:
		if i.from_date == i.to_date:
			leave_dates.append(datetime.combine(i.to_date, datetime.min.time()))
		else:
			date = get_date_range(from_date = i.from_date, to_date = i.to_date)
			for j in date:
				leave_dates.append(datetime.combine(j,datetime.min.time()))
	return leave_dates

def get_date_range(from_date, to_date):
	print("get_date_range")
	days = to_date - from_date
	dates = []
	for i in range(days.days + 1):
		day = from_date + timedelta(days=i)
		dates.append(day)
	return dates

def get_data(filters=None):
	data = []
	y,n = 'Y','N'
	filter_keys = list(filters.keys())
	if 'employee_id' not in filter_keys or 'from_date' not in filter_keys or 'to_date' not in filter_keys:
		return 0
	to_date = datetime.strptime(filters.to_date, "%Y-%m-%d")
	from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")

	dates = get_date_range(from_date = from_date, to_date = to_date)

	annual_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date, leave_type="Annual Leave")

	sick_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date, leave_type = 'Sick Leave')

	other_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date)

	for i in dates:
		dict = {}
		dict["day"] = i.strftime("%A")
		dict["date"] = i.strftime("%d-%m-%Y")
		dict["annual_leave"] = y if annual_leave and i in annual_leave else n
		dict["sick_leave"] = y if sick_leave and i in sick_leave else n
		dict["other_leave"] = y if other_leave and i in other_leave else n
		data.append(dict)
	return data