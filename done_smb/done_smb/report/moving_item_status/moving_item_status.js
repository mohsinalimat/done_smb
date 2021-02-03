// Copyright (c) 2016, smb and contributors
// For license information, please see license.txt
/* eslint-disable */

frappe.query_reports["Moving Item Status"] = {
	"filters": [
		{
			"fieldname": "from_date",
			"fieldtype": "Date",
			"label": "From Date",
			"mandatory": 1
		},
		{
			"fieldname": "to_date",
			"fieldtype": "Date",
			"label": "To Date",
			"mandatory": 1
		}

	]
};
