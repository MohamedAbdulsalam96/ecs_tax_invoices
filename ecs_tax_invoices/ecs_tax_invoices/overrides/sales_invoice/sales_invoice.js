frappe.ui.form.on("Sales Invoice", {

 make_tax: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "make_tax",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});

frappe.ui.form.on("Sales Invoice", {

 tax_type: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "validate_tax_type",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});

frappe.ui.form.on("Sales Invoice", {

 cancel_tax: function(frm) {
			frappe.call({
				doc: frm.doc,
				method: "cancel_tax",
				callback: function(r) {
					frm.refresh_fields();

				}
			});
	}



});