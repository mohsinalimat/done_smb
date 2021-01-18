// Copyright (c) 2021, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Salary Certificate', {
	onload:function(frm){
		frappe.call({
			method:'done_smb.done_smb.doctype.salary_certificate.salary_certificate.find_role',
			args:{
				'user_mail': frappe.session.user_email,
			},
			callback:function(res){
				if (!res.exc){
					console.log(res.message)
					if(res.message == 'Employee'){
						frappe.call({
							method: 'done_smb.done_smb.doctype.salary_certificate.salary_certificate.getuser',
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
					}
				}
			}
		})

	},
	employee_id:function(frm){
		frappe.call({
			method:'done_smb.done_smb.doctype.salary_certificate.salary_certificate.find_role',
			args:{
				'user_mail': frappe.session.user_email,
			},
			callback:function(res){
				if (!res.exc){
					if(res.message == 'Employee'){
						frappe.call({
							method: 'done_smb.done_smb.doctype.salary_certificate.salary_certificate.getuser',
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
					}
					else if(res.message == "HR"){
						if(frm.doc.employee_id != null){
							frappe.call({
							method: 'done_smb.done_smb.doctype.salary_certificate.salary_certificate.get_name',
							args: {
								'id':frm.doc.employee_id,
							},
							callback:function(res){
								if(!res.exc){
									frm.set_value('employee_name', res.message);
				
								}
							}
						});}
					}			
				}
			}
		})
	}
});
