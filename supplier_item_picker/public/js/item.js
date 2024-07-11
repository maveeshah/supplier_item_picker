
frappe.ui.form.on("Item Barcode", {
    form_render: function (frm, cdt, cdn) {
        var d = locals[cdt][cdn],
            wrapper = frm.fields_dict[d.parentfield].grid.grid_rows_by_docname[cdn].grid_form.fields_dict['custom_test_image'].wrapper;
        var barcode = frappe.model.get_value(cdt, cdn, "custom_barcode_svg");
        if (barcode) {
            $(wrapper).html("<img src='" + barcode + "'>");
        }

    },
    custom_create_barcode: function (frm, cdt, cdn) {
        frappe.call({
            method: "supplier_item_picker.api.create_code",
            args: {
                'number': frm.cur_grid.doc.barcode,
                'item_code': frm.fields_dict.item_code.value,
                'item_name': frm.fields_dict.item_name.value

            },
            callback: function (r) {
                frappe.model.set_value(cdt, cdn, "barcode", r.message.message.barcode);

                frappe.model.set_value(cdt, cdn, "custom_barcode_svg", r.message.message.image);

                frappe.model.set_value(cdt, cdn, "custom_test_image", "<img src='" + r.message.message.image + "'>");

                var d = locals[cdt][cdn],
                    wrapper = frm.fields_dict[d.parentfield].grid.grid_rows_by_docname[cdn].grid_form.fields_dict['custom_test_image'].wrapper;
                $(wrapper).html("<img src='" + r.message.message.image + "'>");
            }
        });
    }
});