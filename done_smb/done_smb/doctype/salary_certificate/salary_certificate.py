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

class SalaryCertificate(Document):
	pass
