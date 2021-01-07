// Copyright (c) 2021, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Certificate', {
	onload:function(frm){
		console.log("loaded")
		frappe.call({
			method: 'erpnext.hr.doctype.salary_certificate.salary_certificate.getuser',
			args: {
				'user':frappe.session.user_email,
			},
			callback:function(res){
				if(!res.exc){
					console.log(res.message)
					frm.set_value('employee_id', res.message[0].name);
					frm.set_value('employee_name', res.message[0].employee_name);

				}
			}
		});
	},
});
