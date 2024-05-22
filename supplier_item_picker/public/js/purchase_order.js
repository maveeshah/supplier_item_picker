frappe.ui.form.on("Purchase Order", {
  refresh: function (frm) {
    if (frm.doc.docstatus === 0 && !frm.doc.is_return) {
      frm.add_custom_button(__("Fetch Supplier Items"), function () {
        let supplier = frm.doc.supplier;
        if (!supplier) {
          frappe.msgprint(__("Please select a supplier first."));
          return;
        }
        let filters = { supplier: supplier };
        fetch_supplier_items(frm, filters);
      });
    }
  },
});

function fetch_supplier_items(frm, filters) {
  frappe.call({
    method: "supplier_item_picker.api.get_items",
    args: filters,
    callback: function (r) {
      if (r.message && r.message.length > 0) {
        select_items_dialog(frm, r.message);
      } else {
        frappe.msgprint(__("No items found for the selected supplier."));
      }
    },
  });
}

function select_items_dialog(frm, items) {
    const fields = [
      {
        fieldtype: "HTML",
        fieldname: "items_list",
        label: __("Items"),
        options: "Loading...",
      },
    ];
  
    const item_dialog = new frappe.ui.Dialog({
      title: __("Select Items"),
      fields: fields,
    });
  
    const item_html_field = item_dialog.fields_dict.items_list.$wrapper;
    item_html_field.empty();
  
    // Construct a table with the items and a "Select All" checkbox
    const table_html = `
          <div class="table-responsive">
              <table class="table table-bordered table-hover">
                  <thead>
                      <tr>
                          <th><input type="checkbox" id="select-all-items" /> ${__("Select All")}</th>
                          <th>${__("Item Name")}</th>
                      </tr>
                  </thead>
                  <tbody>
                      ${items
                        .map(
                          (item) => `
                          <tr>
                              <td><input type="checkbox" data-item-name="${item.parent}" class="item-check"></td>
                              <td>${item.parent}</td>
                          </tr>
                      `
                        )
                        .join("")}
                  </tbody>
              </table>
          </div>
      `;
  
    item_html_field.html(table_html);
  
    // Add event listener for "Select All" checkbox
    item_html_field.find("#select-all-items").on("change", function () {
      const is_checked = $(this).is(":checked");
      item_html_field.find(".item-check").prop("checked", is_checked);
    });
  
    item_dialog.set_primary_action(__("Add Selected Items"), function () {
      const selected_items = [];
      item_html_field.find(".item-check:checked").each(function () {
        selected_items.push($(this).data("item-name"));
      });
  
      if (selected_items.length > 0) {
        add_selected_items_to_form(frm, selected_items);
        item_dialog.hide();
      } else {
        frappe.msgprint(__("Please select at least one item."));
      }
    });
  
    item_dialog.show();
  }
  
function add_selected_items_to_form(frm, selected_items) {
  frappe.call({
    method: "supplier_item_picker.api.get_items_details",
    args: { items: selected_items },
    callback: function (r) {
      if (r.message && r.message.length > 0) {
        console.log(r.message);
        frm.clear_table("items");
        r.message.forEach((item) => {
          let row = frm.add_child("items");
          row.item_code = item.name;
          row.item_name = item.item_name;
          row.description = item.description || item.item_name;
          row.rate = item.standard_rate || 0;
          row.qty = 1;
          row.schedule_date = frappe.datetime.nowdate()
          row.uom = item.stock_uom;
          frm.refresh_field("items");
        });
      } else {
        frappe.msgprint(
          __("Failed to fetch item details for the selected items.")
        );
      }
    },
  });
}
