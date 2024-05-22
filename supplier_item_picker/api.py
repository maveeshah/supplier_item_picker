import frappe
import json


@frappe.whitelist()
def get_items(supplier):
    """
    Retrieves a list of items associated with a given supplier.

    Args:
        supplier (str): The name of the supplier.

    Returns:
        list: A list of dictionaries representing the items. Each dictionary contains the following keys:
            - name (str): The name of the item.
            - item_name (str): The display name of the item.

    If no items are found for the given supplier, an empty list is returned.
    """
    # Get item codes from Item Supplier
    item_codes = frappe.get_all(
        "Item Supplier", filters={"supplier": supplier}, fields=["parent"]
    )
    item_codes = [item["parent"] for item in item_codes]

    if not item_codes:
        return []

    # Get item names from Item doctype
    items = frappe.get_all(
        "Item", filters={"name": ["in", item_codes]}, fields=["name", "item_name"]
    )

    return items or []  # Return an empty list if no items are found


@frappe.whitelist()
def get_items_details(items):
    """
    Retrieves the details of a list of items.

    Args:
        items (Union[str, List[str]]): A string representing a JSON list of item names, or a list of item names.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries representing the details of the items. Each dictionary contains the following keys:
            - name (str): The name of the item.
            - item_name (str): The display name of the item.
            - ... (Any): Other fields of the Item doctype.

    If no items are found, an empty list is returned.

    """
    if isinstance(items, str):
        items = json.loads(items)
    items = set(items)
    # Fetch details for the items
    items_details = frappe.get_all(
        "Item", filters={"name": ["in", list(items)]}, fields="*"
    )

    return items_details or []  # Return an empty list if no details are found
