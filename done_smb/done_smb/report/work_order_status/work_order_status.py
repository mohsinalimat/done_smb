# Copyright (c) 2013, smb and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe

def execute(filters=None):
	data = []
	if filters.from_date and filters.to_date:
		data = get_data(filters)
	columns = get_columns(filters)
	return columns, data


def get_columns(filters):
	columns = [
	{
		"fieldname":"sales_order",
		"label": "Sales Order",
		"fieldtype": "Data",
	},
	{
		"fieldname":"custom_order_contract",
		"label": "Custom Order Contract",
		"fieldtype": "Data",
	},
	{
		"fieldname":"work_order",
		"label": "Work Order",
		"fieldtype": "Data",
	},
	{
		"fieldname":"status",
		"label": "Work Order Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"count",
		"label": "Count",
		"fieldtype": "Data",
	},
	
	
	]
	return columns

def get_data(filters):
	data = frappe.db.sql(""" 
	select so.name, coc.name, wo.name, wo.status, count(wo.status)
	from `tabSales Order` as so
			left outer join `tabCustom Order Contract` as coc on coc.name = so.coc and coc.docstatus = 1
			left outer join `tabWork Order` as wo on wo.sales_order = so.name and wo.docstatus = 1
	where so.delivery_date >= %s
	and so.delivery_date < %s
	and so.docstatus = 1
	group by so.name, coc.name, wo.name, wo.status
	""",(filters.from_date,filters.to_date),as_list = 1)
	return data

