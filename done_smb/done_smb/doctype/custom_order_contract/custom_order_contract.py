# -*- coding: utf-8 -*-
# Copyright (c) 2021, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document
from json import loads

@frappe.whitelist()
def get_status(name, items, is_report):
	is_report = int(is_report)
	status = {}
	sales_name = frappe.db.get_value("Sales Order", {'coc': name}, ['name'])
	items = loads(items)
	for i in items:
		work = frappe.db.get_value("Work Order", {"production_item": i, "sales_order": sales_name}, ["status"])
		status[i] = work
	print(not is_report)
	if not is_report:
		body = f''
		for i in items:
			body += f'<tr><td style="border: 1px solid black;width:50%">{i}</td><td style="border: 1px solid black;width:50%">{status[i]}</td></tr>'
		table = f'<table width=100%><tr><td style="border: 1px solid black;width:50%;text-align:center"><strong>Items</strong></td><td style="border: 1px solid black;width:50%;text-align:center"><strong>Status</strong></td></tr>{body}</table>'
		print(table)	
		return table
	return status

class CustomOrderContract(Document):
	def on_submit(self):
		if self.make_sales_invoice == 1:
			if self.reference_no == "" or self.reference_no == None:
				frappe.throw("Mandatory field Reference No required in Custom Order Contract")
		so = frappe.new_doc("Sales Order") # sales order
		so.coc = self.name
		for i in range(len(self.item)):
			row = so.append("items",{})
			row.item_code = self.item[i].item
			row.item_name = self.item[i].item_name
			row.qty = self.item[i].qty
		so.save()
		sales_no = so.name
		so.submit()
		for i in range(len(self.item)): # work order
			wo = frappe.new_doc("Work Order")
			wo.production_item = self.item[i].item
			wo.qty = int(self.item[i].qty)
			if frappe.db.exists("BOM",{"item":  self.item[i].item,"docstatus":1,"is_default":1},['name']):
				wo.bom_no = frappe.db.get_value("BOM",{"item":  self.item[i].item,"docstatus":1,"is_default":1},['name'])
			else:
				frappe.throw(f"{self.item[i].item} item has no Default BOM")
			wo.wip_warehouse = "All Warehouses - DI"
			wo.fg_warehouse = "All Warehouses - DI"
			wo.sales_order = sales_no
			wo.save()
			for ware in wo.required_items:
				ware.source_warehouse = "All Warehouses - DI"
			wo.save()
			wo.submit()
		if self.make_sales_invoice == 1:  # sales invoice
			si = frappe.new_doc("Sales Invoice")
			si.customer = self.customer
			si.reference_no = self.reference_no
			for i in self.item:
				row = si.append("items",{})
				row.item_code = i.item	
				row.qty = i.qty
				row.sales_order = sales_no
			si.save()
			si.submit()
		# po = frappe.new_doc("Purchase Order")

		


