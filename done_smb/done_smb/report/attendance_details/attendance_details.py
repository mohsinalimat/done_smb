# Copyright (c) 2013, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from datetime import date, timedelta, datetime

def execute(filters=None):
	columns = [
		{
			"fieldname": "day",
			"fieldtype": "Data",
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
			"fieldname": "employee",
			"fieldtype": "data",
			"label": "Employee Id",
			"width": 0	
		},
		{
			"fieldname": "time_in",
			"fieldtype": "Time",
			"label": "Time IN",
			"width": 0,
		},
		{
			"fieldname": "time_out",
			"fieldtype": "Time",
			"label": "Time OUT",
			"width": 0,
		}, 
		{
			"fieldname": "early_in",
			"fieldtype": "Time",
			"label": "Early IN",
			"width": 0,
		},
		{
			"fieldname": "early_out",
			"fieldtype": "Time",
			"label": "Early OUT",
			"width": 0,
		},
		{
			"fieldname": "late_in",
			"fieldtype": "Time",
			"label": "Late IN",
			"width": 0,
		},
		{
			"fieldname": "late_out",
			"fieldtype": "Time",
			"label": "Late OUT",
			"width": 0,
		},
		{
			"fieldname": "missing_in",
			"fieldtype": "Data",
			"label": "Missing IN",
			"width": 0,
		},
		{
			"fieldname": "missing_out",
			"fieldtype": "Data",
			"label": "Missing OUT",
			"width": 0,
		},
		{
			"fieldname": "permissions",
			"fieldtype": "Data",
			"label": "Permissions",
			"width": 0,
		},
		{
			"fieldname": "official_duties",
			"fieldtype": "Data",
			"label": "Official Duties",
			"width": 0,
		},
		{
			"fieldname": "attended_hours",
			"fieldtype": "Time",
			"label": "Attended Hours",
			"width": 0,
		},
		{
			"fieldname": "working_hours",
			"fieldtype": "Time",
			"label": "Working Hours",
			"width": 0,
		},
		{
			"fieldname": "annual_leave",
			"fieldtype": "Data",
			"label": "Annual Leave",
			"width": 0,
		},
		{
			"fieldname": "sick_leave",
			"fieldtype": "Data",
			"label": "Sick Leave",
			"width": 0,
		},
		{
			"fieldname": "other_leave",
			"fieldtype": "Data",
			"label": "Other Leave",
			"width": 0,
		},
		{
			"fieldname": "official_duty",
			"fieldtype": "Data",
			"label": "Official Duty",
			"width": 0,
		},
		{
			"fieldname": "training_course",
			"fieldtype": "Data",
			"label": "Training course",
			"width": 0,
		},
		{	
			"fieldname": "business_trip",
			"fieldtype": "Data",
			"label": "Business Trip",
			"width": 0,
		},
		{
			"fieldname": "absence",
			"fieldtype": "Data",
			"label": "Absence",
			"width": 0,
		},
		{
			"fieldname": "avg_attendance",
			"fieldtype": "Percent",
			"label": "Avg Attendance%",
			"precision": "2",
			"width": 0,
		},
		{
			"fieldname": "extra_hour_avg_attendance",
			"fieldtype": "Percent",
			"label": "Extra Hours Avg Attendance%",
			"precision": "2",
			"width": 0,
		}
	]
	filter_keys = list(filters.keys())
	data = []
	if 'employee_id' in filter_keys and'from_date' in filter_keys and 'to_date' in filter_keys:
		data = get_data(filters)
	elif 'from_date' in filter_keys and 'to_date' in filter_keys:
		data = get_all_data(filters)

	return columns, data

def get_all_data(filters):
	employee = frappe.db.get_list("Employee", order_by='name')
	result = []
	filters['employee_id'] = ""
	for i in employee:
		filters['employee_id'] = i.name
		print(i.name)
		for j in get_data(filters):
			result.append(j)
		result.append({})
	return result

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
	days = to_date - from_date
	dates = []
	for i in range(days.days + 1):
		day = from_date + timedelta(days=i)
		dates.append(day)
	return dates

def get_data(filters=None):
	data = []
	y,n = 'Y','N'
	to_date = datetime.strptime(filters.to_date, "%Y-%m-%d")
	from_date = datetime.strptime(filters.from_date, "%Y-%m-%d")

	dates = get_date_range(from_date = from_date, to_date = to_date)

	annual_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date, leave_type="Annual Leave")

	sick_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date, leave_type = 'Sick Leave')

	other_leave = get_leave(emp_id = filters.employee_id, from_date = filters.from_date, to_date = filters.to_date)

	setting = frappe.get_doc("Attendance Setting")
	shift_in_time = datetime.strptime(setting.start_time, "%H:%M:%S")
	shift_out_time = datetime.strptime(setting.end_time, "%H:%M:%S")
	working_hours =  shift_out_time - shift_in_time
	for i in dates:
		attendance = frappe.db.get_list("Attendance", filters=[["employee", "=", filters.employee_id], ["attendance_date", "=", i]], fields=['status', 'in_time', 'out_time']) 
		dict = {}
		dict["day"] = i.strftime("%A")
		dict["date"] = i.strftime("%d-%m-%Y")
		if dict["day"] == 'Friday':
			data.append(dict)
			continue
		dict['employee'] = filters.employee_id
		if attendance and attendance[0]['status']== 'Present':
			in_time = datetime.strptime(attendance[0].in_time, "%H:%M:%S")
			out_time = datetime.strptime(attendance[0].out_time, "%H:%M:%S")
			dict['time_in'] = in_time.strftime("%H:%M:%S")
			dict['time_out'] = out_time.strftime("%H:%M:%S")
			print("haaaaaai")
			print(shift_out_time, out_time, out_time < shift_out_time, shift_out_time - out_time)
			if in_time < shift_in_time:
				print(shift_in_time - in_time)
				dict['early_in'] = shift_in_time - in_time
			elif in_time > shift_in_time:
				dict['late_in'] = in_time - shift_in_time
			
			if out_time < shift_out_time:
				print("inned")
				dict['early_out'] = shift_out_time - out_time
				print
			elif out_time > shift_out_time:
				dict['late_out'] = out_time - shift_out_time

			dict['missing_in'] = y if not in_time else n
			dict['missing_out'] = y if not out_time else n

			dict['attended_hours'] = out_time - in_time
			att_hrs = (out_time - in_time).total_seconds()
			dict['working_hours'] = working_hours
			work_hrs = working_hours.total_seconds()
			extra = 0
			if in_time < shift_in_time or out_time > shift_out_time:
				dict['extra_hour_avg_attendance'] = timedelta(100 * ( dict['early_in'] + dict['late_out']).total_seconds() / work_hrs)
				extra = 100 * ( dict['early_in'] + dict['late_out']).total_seconds() / work_hrs
			dict['avg_attendance'] = timedelta(100 * att_hrs / work_hrs - extra)
		else:
			dict['time_in'] = n
			dict['time_out'] = n
			dict['early_in'] = n
			dict['early_out'] = n
			dict['late_in'] = n
			dict['late_out'] = n
			dict['missing_in'] = n
			dict['missing_out'] = n
			dict['attended_hours'] = n
			dict['working_hours'] = n
			if annual_leave and i in annual_leave:
				dict["annual_leave"] = y
				dict["sick_leave"] = n
				dict["other_leave"] = n
				dict['absence'] = n
			elif sick_leave and i in sick_leave:
				dict["sick_leave"] = y
				dict["annual_leave"] = n
				dict["other_leave"] = n
				dict['absence'] = n
			elif other_leave and i in other_leave:
				dict["other_leave"] = y
				dict["annual_leave"] = n
				dict["sick_leave"] = n
				dict['absence'] = n
			else:
				dict["annual_leave"] = n
				dict["sick_leave"] = n
				dict["other_leave"] = n
				dict['absence'] = y
		data.append(dict)
	return data