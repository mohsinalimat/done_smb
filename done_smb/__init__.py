# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import math
from erpnext.hr.doctype.leave_application.leave_application import get_holidays
from erpnext.hr.doctype.leave_application.leave_application import get_leave_details
from frappe.utils import date_diff
from datetime import datetime, date

__version__ = '0.0.1'
from datetime import date
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


def get_date():
	return date.today().strftime("%d-%m-%Y")

def get_details(emp_id):
	return frappe.db.sql("select designation, date_of_joining from `tabEmployee` where name=%s",(emp_id),as_dict =1)

def salary_detail(emp_id):
	salary = {}
	salary["amount"] = frappe.db.get_value("Salary Structure Assignment",{"employee":emp_id},["base"])
	salary["words"] =  frappe.utils.money_in_words(salary["amount"])
	return salary

def employee_detail_arabic(doc):
	name = ""
	if doc.arabic_name1:
		name = name + doc.arabic_name1
	if doc.arabic_name2:
		name = name + doc.arabic_name2
	if doc.arabic_name3:
		name = name + doc.arabic_name3
	if doc.arabic_name4:
		name = name + doc.arabic_name4 
	return name

def annual_leave_form(emp_id, leave_type, from_d, to_d, pos_d):
	leave = {}
	leave["to_be_paid"] = "Unpaid" if frappe.db.get_value("Leave Type",leave_type,"is_lwp") else "Paid"
	leave["holidays"] = get_holidays(emp_id,leave_type,from_d,to_d)
	leave["no_of_days"] = date_diff(to_d,from_d) + 1
	balance = get_leave_details(emp_id,pos_d)
	balance_count = 0
	for types in balance["leave_allocation"]:
		balance_count += balance["leave_allocation"][types]["remaining_leaves"]
	leave["balance"] = balance_count
	paid_leaves = 0
	unpaid_leaves = 0
	paid_salary = 0
	if frappe.db.get_value("Leave Type",leave_type,"is_lwp"):
		unpaid_leaves = leave["no_of_days"]
	else:
		paid_leaves = leave["no_of_days"]
		if leave_type == "25 Percent unpaid Sick":
			paid_salary = (salary_detail(emp_id)["amount"] / 26) * leave["no_of_days"] * 0.25
		elif leave_type == "50 Percent unpaid Sick":
			paid_salary = (salary_detail(emp_id)["amount"] / 26) * leave["no_of_days"] * 0.50
		elif leave_type == "75 Percent unpaid Sick":
			paid_salary = (salary_detail(emp_id)["amount"] / 26) * leave["no_of_days"] * 0.75
		else:
			paid_salary = (salary_detail(emp_id)["amount"] / 26) * leave["no_of_days"]
	leave["paid_leaves"] = paid_leaves
	leave["unpaid_leaves"] = unpaid_leaves
	leave["paid_salary"] = math.ceil(paid_salary)
	leave["remaining"] = leave["balance"] - leave["no_of_days"]
	leave["bank"] = "N/A"
	leave["account"] = "N/A"
	mode = frappe.db.get_value("Employee",emp_id,"bank_name")
	if mode == "Bank":
		leave["bank"] =  mode
		leave["account"] = frappe.db.get_value("Employee",emp_id,"bank_ac_no")
	leave["table_paid_leaves"] = {}
	leave["table_unpaid"] = {}
	leave["table_paid_leaves"]["date_from"] = ""
	leave["table_paid_leaves"]["date_to"] = ""
	leave["table_paid_leaves"]["total"] = ""
	leave["table_paid_leaves"]["holiday"] = ""
	leave["table_paid_leaves"]["net"] = ""
	leave["table_paid_leaves"]["offical"] = ""
	leave["table_unpaid"]["date_from"] = ""
	leave["table_unpaid"]["date_to"] = ""
	leave["table_unpaid"]["total"] = ""
	if leave["to_be_paid"] == "Paid":
		leave["table_paid_leaves"]["date_from"] = from_d
		leave["table_paid_leaves"]["date_to"] = to_d
		leave["table_paid_leaves"]["total"] = leave["no_of_days"]
		leave["table_paid_leaves"]["holiday"] = leave["holidays"]
		leave["table_paid_leaves"]["net"] = leave["no_of_days"] - leave["holidays"]
		leave["table_paid_leaves"]["offical"] = 0
	else:
		leave["table_unpaid"]["date_from"] = from_d
		leave["table_unpaid"]["date_to"] = to_d
		leave["table_unpaid"]["total"] = leave["no_of_days"]
	
	return leave

def get_allowence(sal_stuct):
	sal_detail = frappe.get_doc("Salary Structure", sal_stuct)
	allow = 0
	for i in sal_detail.earnings:
		if i.salary_component != 'Basic':
			allow = allow + i.amount
	return allow

def get_sick_leave(employee, start, end):
	leave = ['Sick Leave Unpaid', '25 Percent unpaid Sick', '75 Percent unpaid Sick', '50 Percent unpaid Sick', 'Sick Leave']
	leave_days = 0
	for typ in leave:
		list = frappe.db.get_list("Leave Application", filters=[
				['status', '=', 'Approved'],
				['posting_date', '>=', start],
				['posting_date', '<', end], 
				['employee', '=', employee],
				['leave_type', '=', typ]
			], fields=["total_leave_days"])
		leave_days += sum([i.total_leave_days for i in list])
	return leave_days

def send_mail(recipients, subject, message):
	frappe.sendmail(
				recipients = recipients,
				subject = subject,
				message = message
			)
	# frappe.sendmail(recipients = recipients, subject = subject, message = message)

def late_entry():
	late_entry = []
	early_out = []
	today = date.today()
	shift = frappe.get_doc("Attendance Setting")
	shift_in_time = datetime.strptime(shift.start_time, "%H:%M:%S")
	shift_out_time = datetime.strptime(shift.end_time, "%H:%M:%S")
	
	attendance = frappe.db.get_list("Attendance", {"attendance_date":today}, ["employee", "employee_name", "in_time", "out_time"])
	for emp in attendance:
		in_time = datetime.strptime(attendance[0].in_time, "%H:%M:%S")
		out_time = datetime.strptime(attendance[0].out_time, "%H:%M:%S")
		mail = frappe.db.get_value("Employee", emp.employee, "user_id")
		if in_time > shift_in_time:
			dic = {}
			dic["employee"] = emp.employee
			dic["employee_name"] = emp.employee_name
			dic["late_time"] = in_time - shift_in_time
			late_entry.append(dic)
			if mail:
				send_mail(recipients=mail, subject= "Reg Late Entry", message=f"{emp.employee} {emp.employee_name} came {emp.late_time} hr late Today")			

		if out_time < shift_out_time:
			dic = {}
			dic['employee'] = emp.employee
			dic["employee_name"] = emp.employee_name
			dic["early_out"] = shift_out_time - out_time
			early_out.append(dic)
			if mail:
				send_mail(recipients=mail, subject= "Reg Early Exit", message=f"{emp.employee} {emp.employee_name} gone {emp.late_time} hr early Today")

	if len(late_entry)!=0 or len(early_out)!=0:
		late = ''
		for  i in late_entry:
			late += f"<tr><td>{i['employee']}</td><td>{i['employee_name']}</td><td>{i['late_time']}</td></tr>"
		early = ''
		for  i in early_out:
			early += f"<tr><td>{i['employee']}</td><td>{i['employee_name']}</td><td>{i['early_out']}</td></tr>"
	
		late_tbl = f'<table><tr><td style="width:30%">Employee Id</td><td style="width:40%">Employee Name</td><td style="width:30%">Late Entry Time</td></tr>{late}</table>'
		early_tbl = f'<table><tr><td style="width:30%">Employee Id</td><td style="width:40%">Employee Name</td><td style="width:30%">Early Exit Time</td></tr>{early}</table>'
		content = f'<table><tr><td style="width:50%">Late Entry</td><td style="width:50%">Early Exit</td></tr><tr"><td>{late_tbl}</td><td>{early_tbl}</td></table>'


		hr_mail = get_hr_mail()
		send_mail(recipients= hr_mail, subject="Reg Late Entries and early exits", message=content)

		frappe.db.commit()

@frappe.whitelist()
def get_hr_mail():
	all_mail = frappe.db.sql("""SELECT DISTINCT a.parent FROM `tabHas Role` as a inner join `tabUser` as b on a.parent = b.name  WHERE role={role} and a.parent != 'Administrator'""".format(role="\'HR Manager\'"), as_list=1)
	return [ i[0] for i in all_mail]


def set_value_contract(doc , action):
	if not action == 'validate':
		return 
	cus_record = frappe.db.sql("select customer_name ,mobile_no, email_id , address_html from `tabCustomer` where name = %s",(doc.party_name),as_dict = 1)
	print(cus_record)
	doc.contract_terms = (doc.contract_terms).format(cus_record[0]['customer_name'], doc.civil_id, "Country", doc.mobile_no , cus_record[0]['email_id'], "Civic Id country issuer", cus_record[0]['address_html'])
	# doc.save()
