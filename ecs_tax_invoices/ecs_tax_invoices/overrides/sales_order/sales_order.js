frappe.ui.form.on("Sales Order", {

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