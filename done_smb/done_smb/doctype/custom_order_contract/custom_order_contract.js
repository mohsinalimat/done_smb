// Copyright (c) 2021, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custom Order Contract', {
	refresh: function(frm) {
		var item = []
		for(var i in frm.doc.item){
			item.push(frm.doc.item[0]['item']);
		}
		frappe.call({
			'method': 'done_smb.done_smb.doctype.custom_order_contract.custom_order_contract.get_status',
			'args': {
				"name": frm.doc.name,
				"items": item,
				"is_report": 0
			},
			callback: function(res){
				if(!res.exc){
					frm.set_value('work_order_status', res.message);
				}
			}
		})
	}
});
