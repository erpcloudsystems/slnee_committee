// Copyright (c) 2021, ERPCloud.Systems and contributors
// For license information, please see license.txt


frappe.ui.form.on('Committee Meeting', {
    get_requests: function(frm) {
            cur_frm.clear_table("requests_table");
			frappe.call({
				doc: frm.doc,
				method: "get_requests",
				    callback: function(r) {
                    refresh_field("requests_table");
                    refresh_field("committee_members");
                    cur_frm.save('Save');
                }
			});
	}

})

frappe.ui.form.on('Committee Meeting', {
    get_members: function(frm) {
            cur_frm.clear_table("committee_members");
			frappe.call({
				doc: frm.doc,
				method: "get_members",
				    callback: function(r) {
				    refresh_field("requests_table");
                    refresh_field("committee_members");
                }
			});
	}
})

frappe.ui.form.on('Committee Meeting',  'validate',  function(frm) {
    if (cur_frm.doc.meeting_status == "Closed") {
        cur_frm.set_value("color", "#ff9e9e");
    }
    else {
    cur_frm.set_value("color", "#449CF0");
    }
});

frappe.ui.form.on('Committee Meeting',  'meeting_status',  function(frm) {
    if (cur_frm.doc.meeting_status == "Closed") {
        cur_frm.set_value("color", "#ff9e9e");
    }
    else {
    cur_frm.set_value("color", "#449CF0");
    }
});