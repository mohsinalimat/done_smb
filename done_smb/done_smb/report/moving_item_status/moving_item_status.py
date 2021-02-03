# Copyright (c) 2013, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data = []
	columns = [
		{
			"fieldname": "item_code",
			"fieldtype": "Link",
			"label": "Item Code",
			"width": 0,
			"options": "Item"
		},
		{
			"fieldname": "item_name",
			"fieldtype": "Data",
			"label": "Item Name",
			"width": 0
		},
		 {
		 	"fieldname": "item_group",
		 	"fieldtype": "Data",
		 	"label": "Item Group",
		 	"width": 0
		},
		{
			"fieldname": "uom",
			"fieldtype": "data",
			"label": "UOM",
			"width": 0
		},
		{
			"fieldname": "qty",
			"fieldtype": "Data",
			"label": "Quantity",
			"width": 0
		},
		
		
	]
	if filters.from_date and filters.to_date:
		print(filters)
		data = get_data(filters.from_date, filters.to_date)
	return columns, data

def get_data(from_date, to_date):
	print(from_date, to_date)
	data = frappe.db.sql(''' select sii.item_code, sii.item_name, sii.item_group, sii.stock_uom, sum(sii.stock_qty) from `tabSales Invoice Item` as sii inner join `tabSales Invoice` as si on si.name = sii.parent where si.posting_date >= %s and si.posting_date <= %s group by  sii.item_code, sii.item_name, sii.item_group, sii.stock_uom order by sum(sii.stock_qty) DESC''',(from_date, to_date),as_list =1)
	print("~~~~~~~~~~~~~~",data)
	return data