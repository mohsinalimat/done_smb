# -*- coding: utf-8 -*-
# Copyright (c) 2021, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe.model.document import Document

class CustomOrderContract(Document):
	def on_submit(self):
		so = frappe.new_doc("Sales Order")
		so.coc = self.name

		for i in range(len(self.item)):
			row = so.append("items",{})
			row.item_code = self.item[i].item
			row.item_name = self.item[i].item_name
			row.qty = self.item[i].qty
		so.save()
		so.submit()
		for i in range(len(self.item)):
			wo = frappe.new_doc("Work Order")
			wo.production_item = self.item[i].item
			wo.qty = int(self.item[i].qty)
			wo.bom_no = frappe.db.get_value("BOM",{"item":  self.item[i].item,"is_default":1},['name'])
			wo.wip_warehouse = "All Warehouses - DI"
			wo.fg_warehouse = "All Warehouses - DI"
			wo.save()
			for ware in wo.required_items:
				# row = so.append("Work Order Item",{})
				ware.source_warehouse = "All Warehouses - DI"
			wo.save()
			wo.submit()

		

