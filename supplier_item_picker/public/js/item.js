
frappe.ui.form.on("Item Barcode", {
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
                html = `<div><html><img src="data:image/png;base64,${r.message.message.image}"/></html></div>`;
                console.log(html);
                frappe.model.set_value(cdt, cdn, "custom_test_image", html);
            }
        });
    }
});