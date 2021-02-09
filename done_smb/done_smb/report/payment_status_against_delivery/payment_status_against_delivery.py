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
		"fieldtype": "Link",
		"options" : "Sales Order"
	},
	{
		"fieldname":"custom_order_contract",
		"label": "Custom Order Contract",
		"fieldtype": "Link",
		"options" : "Custom Order Contract"

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
	{
		"fieldname":"total_amount",
		"label": "Grand Total",
		"fieldtype": "Data",
	},
	{
		"fieldname":"payment_status",
		"label": "Payment Status",
		"fieldtype": "Data",
	},
	{
		"fieldname":"outstanding",
		"label": "Outstanding",
		"fieldtype": "Data",
	},
	
	
	]
	return columns

def get_data(filters):
	data = frappe.db.sql(""" 
	select result.so,
       result.coc,
       result.status,
       count(result.status),
       result.grand_total,
       result.si,
       result.outstanding_amount
from (select so.name   as so,
             coc.name  as coc,
             wo.name   as wo,
             wo.status,
             si.status as si,
             si.grand_total,
             si.outstanding_amount
      from `tabSales Order` as so
               left outer join `tabCustom Order Contract` as coc on coc.name = so.coc and coc.docstatus = 1
               left outer join `tabWork Order` as wo on wo.sales_order = so.name and wo.docstatus = 1
               inner join `tabSales Invoice Item` as soi on soi.sales_order = so.name
               inner join `tabSales Invoice` as si on si.name = soi.parent and soi.docstatus = 1
		where so.delivery_date >= %s
		and so.delivery_date < %s
		and so.docstatus = 1
      group by so.name, wo, wo.status) as result
group by result.coc, result.so, result.status
	""",(filters.from_date,filters.to_date),as_list = 1)
	return data
