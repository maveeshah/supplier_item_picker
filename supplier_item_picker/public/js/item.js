frappe.ui.form.on('Item', {
    refresh: function (frm) {
        frm.add_custom_button(__('Generate Barcode from Item Name'), function () {
            var cur_doc = frm.doc;
            if (cur_doc.name) {
                $(frm.fields_dict['custom_barcode_image'].wrapper).html('<svg id="ean13"></svg>');
                $.getScript("https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js", function (data, textStatus, jqxhr) {
                    JsBarcode("#ean13", cur_doc.name, {
                        background: "#FFFFFF"
                    });
                    var svg = $('#ean13').parent().html();
                    frappe.model.set_value(cur_doc.doctype, cur_doc.name, "custom_barcode_svg", svg);
                    frappe.model.set_value(cur_doc.doctype, cur_doc.name, "custom_barcode_generated", 1);
                    cur_frm.save();
                });
            } else {
                frappe.msgprint(__("Please enter Barcode to to be printed"));
            }

            //     var item_name = frm.doc.item_name;

            //     if (item_name) {
            //         var barcodeFieldWrapper = $(frm.fields_dict.barcodes.wrapper);
            //         var barcodeTable = barcodeFieldWrapper.find('.form-inner-toolbar').next('.form-grid').find('.grid-body');

            //         // Create a new row in the barcodes table
            //         var newRow = $('<div class="grid-row" data-idx="0"></div>').appendTo(barcodeTable);
            //         var cellWrapper = $('<div class="grid-static-col col col-xs-6 col-sm-6 col-md-6 col-lg-6"></div>').appendTo(newRow);

            //         // Add the custom_barcode_image field to the new row
            //         var imageField = $('<img class="frappe-control">').appendTo(cellWrapper);

            //         // Load JsBarcode script
            //         $.getScript("https://cdn.jsdelivr.net/npm/jsbarcode@3.11.5/dist/JsBarcode.all.min.js", function (data, textStatus, jqxhr) {
            //             try {
            //                 JsBarcode(imageField[0], item_name, {
            //                     format: 'CODE128', // You can use other formats as needed
            //                     lineColor: "#000",
            //                     width: 2,
            //                     height: 100,
            //                     displayValue: true,
            //                     background: "#FFFFFF"
            //                 });
            //                 console.log('hi');
            //                 console.log('Generated Barcode Image Data:', imageField[0].src);
            //                 // Set the item_name as the barcode value
            //                 frm.doc.barcodes[0].custom_barcode_image = imageField[0].src;
            //                 frm.refresh_field('barcodes');
            //             } catch (error) {
            //                 frappe.msgprint(__('Error generating barcode: {0}', [error.message]));
            //             }
            //         });
            //     } else {
            //         frappe.msgprint(__('Please enter the item name.'));
            //     }
        });
    }
});