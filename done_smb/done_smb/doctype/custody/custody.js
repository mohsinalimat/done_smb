// Copyright (c) 2021, smb and contributors
// For license information, please see license.txt

frappe.ui.form.on('Custody', {
	onload: function(frm) {
		frm.fields_dict['custody_item'].grid.get_field('item').get_query = function(doc){
			return{
				filters:{
					"item_group": "Custody Items"
				}
			}
		}
	}
});
