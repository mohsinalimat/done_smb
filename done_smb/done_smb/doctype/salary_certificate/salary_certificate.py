# -*- coding: utf-8 -*-
# Copyright (c) 2021, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

@frappe.whitelist()
def getuser(user):
	emp = frappe.db.get_list("Employee", filters={'user_id':['=',user]}, fields=['name','employee_name'])
	return emp

@frappe.whitelist()
def get_name(id):
	return frappe.db.get_value("Employee", id, 'employee_name')

@frappe.whitelist()
def find_role(user_mail):
	mail = frappe.db.sql("""SELECT DISTINCT a.parent FROM `tabHas Role` as a inner join `tabUser` as b on a.parent = b.name  WHERE role={role} and a.parent != 'Administrator'""".format(role="\'HR Manager\'"), as_list=1)
	mail_list = [ i[0] for i in mail]
	return 'HR' if user_mail in mail_list else 'Employee'
class SalaryCertificate(Document):
	pass
