# -*- coding: utf-8 -*-
# Copyright (c) 2021, Aerele Technologies Private Limited and Contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from frappe.utils import today
import datetime
from dateutil.relativedelta import relativedelta

def calculate_indemnity(employee):
	if not frappe.db.exists('Employee', employee):
		return 0

	data_of_joining = frappe.db.get_value('Employee', employee, 'date_of_joining')
	data_of_end = frappe.db.get_value('Employee', employee, 'relieving_date')
	if not data_of_joining:
		return 0

	if not data_of_end:
		data_of_end = today()

	total_years = relativedelta(datetime.date(data_of_end), datetime.date(data_of_joining)).years

	salary = 0
	net_pay = frappe.db.sql("select net_pay from `tabSalary Slip` where employee = '"+ employee +"' order by posting_date DESC limit 1 ")
	if net_pay:
		salary = net_pay[0][0]

	total_indemnity = 0 

	# less than 3 years no indemnity 
	if total_years < 3:
		return total_indemnity

	# For 3-5 years of work 
	if 3 <= total_years <=5:
		total_indemnity=flt(flt(salary) * flt(total_years) * 15/26)

	# For greater than 5 years of work 
	if total_years > 5:
		over_5_years = total_years - 5 
		indemnity_for_five_years = round(flt(flt(salary) * 5 * 15/26),3)

		indemnity_more_than_5 = round(flt(flt(salary)* over_5_years * 26/26),3)

		total_indemnity = indemnity_for_five_years + indemnity_more_than_5

	return total_indemnity
	
