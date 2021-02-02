// Copyright (c) 2016, smb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Payment Status Against Delivery"] = {
	"filters": [
		{
			"fieldname":"from_date",
			"label": __("From Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1
		},
		{
			"fieldname":"to_date",
			"label": __("To Date"),
			"fieldtype": "Date",
			"width": "80",
			"reqd": 1,
			// "default": frappe.datetime.get_today(),
		},

	]
};
