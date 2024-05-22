import frappe
import json
@frappe.whitelist()
def get_items(supplier):
    items = frappe.get_all('Item Supplier', filters={'supplier': supplier}, fields='parent')
    return items or []  # Return an empty list if no items are found

@frappe.whitelist()
def get_items_details(items):
    if isinstance(items, str):
        items = json.loads(items)
    items = set(items)
    # Fetch details for the items
    items_details = frappe.get_all('Item', filters={'name': ['in', list(items)]}, fields='*')


    return items_details or []  # Return an empty list if no details are found
