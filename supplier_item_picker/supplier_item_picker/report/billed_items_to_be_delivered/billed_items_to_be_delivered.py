import frappe
from frappe.utils import flt  # type: ignore
from frappe import _


def execute(filters=None):
    """
    Executes the report and returns the columns and data for the report.

    Args:
        filters (dict, optional): A dictionary containing the filters to be applied to the report. Defaults to None.

    Returns:
        tuple: A tuple containing the columns and data for the report. The columns is a list of dictionaries representing the columns of the report, and the data is a list of dictionaries representing the rows of the report.
    """
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
    """
    Returns a list of dictionaries representing the columns of the report.

    Each dictionary in the list contains the following keys:
    - label: The label of the column.
    - fieldname: The field name of the column.
    - fieldtype: The field type of the column.
    - options: The options for the field (if applicable).
    - width: The width of the column.

    Returns:
    - A list of dictionaries representing the columns of the report.
    """
    return [
        {
            "label": _("Sales Invoice"),
            "fieldname": "sales_invoice",
            "fieldtype": "Link",
            "options": "Sales Invoice",
            "width": 175,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 175,
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 150,
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 150,
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 150,
        },
        {
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
            "options": "UOM",
            "width": 100,
        },
        {
            "label": _("Billed Qty"),
            "fieldname": "billed_qty",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("Delivered Qty"),
            "fieldname": "delivered_qty",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("Pending Delivery Qty"),
            "fieldname": "pending_delivery_qty",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("Rate"),
            "fieldname": "rate",
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "label": _("Amount"),
            "fieldname": "amount",
            "fieldtype": "Currency",
            "width": 150,
        },
    ]


def get_report_filters(report_filters):
    """
    Generate the report filters based on the given report filters.

    Args:
        report_filters (dict): A dictionary containing the report filters.
            It should have the following keys:
            - company (str): The company name.
            - posting_date (str): The posting date.
            - sales_invoice (str, optional): The sales invoice name.

    Returns:
        list: A list of filters to be used in the report. Each filter is a list
            with the following format:
            - [doctype, fieldname, condition, value]
    """
    filters = [
        ["Sales Invoice", "company", "=", report_filters.get("company")],
        ["Sales Invoice", "posting_date", "<=", report_filters.get("posting_date")],
        [
            "Sales Invoice",
            "update_stock",
            "=",
            report_filters.get("stock_updated"),
        ],
        ["Sales Invoice", "docstatus", "=", 1],
    ]

    if report_filters.get("sales_invoice"):
        filters.append(
            ["Sales Invoice", "name", "=", report_filters.get("sales_invoice")]
        )

    if report_filters.get("customer"):
        filters.append(
            ["Sales Invoice", "customer", "=", report_filters.get("customer")]
        )

    return filters


def get_data(filters):
    """
    Retrieves data based on the given filters.

    Args:
        filters (dict): A dictionary containing the filters for the data retrieval.

    Returns:
        list: A list of dictionaries representing the retrieved data. Each dictionary contains the following keys:
            - sales_invoice (str): The name of the sales invoice.
            - customer (str): The name of the customer.
            - posting_date (str): The posting date of the sales invoice.
            - item_code (str): The code of the item.
            - item_name (str): The name of the item.
            - uom (str): The unit of measurement for the item.
            - billed_qty (float): The quantity of the item billed.
            - delivered_qty (float): The quantity of the item delivered.
            - pending_delivery_qty (float): The quantity of the item pending delivery.
            - rate (float): The rate of the item.
            - amount (float): The amount of the item.
    """
    filters = get_report_filters(filters)
    data = []
    sales_invoices = frappe.get_all(
        "Sales Invoice", filters=filters, fields=["name", "customer", "posting_date"]
    )

    for invoice in sales_invoices:
        items = frappe.get_all(
            "Sales Invoice Item",
            filters={"parent": invoice.name},
            fields=["item_code", "item_name", "qty", "uom", "rate", "amount"],
        )

        for item in items:
            delivered_qty = (
                frappe.db.sql(
                    """
                SELECT SUM(qty)
                FROM `tabDelivery Note Item`
                WHERE docstatus = 1
                AND against_sales_invoice = %s
                AND item_code = %s
            """,
                    (invoice.name, item.item_code),
                )[0][0]
                or 0
            )

            pending_delivery_qty = flt(item.qty) - flt(delivered_qty)
            if pending_delivery_qty > 0:
                data.append(
                    {
                        "sales_invoice": invoice.name,
                        "customer": invoice.customer,
                        "posting_date": invoice.posting_date,
                        "item_code": item.item_code,
                        "item_name": item.item_name,
                        "uom": item.uom,
                        "billed_qty": item.qty,
                        "delivered_qty": delivered_qty,
                        "pending_delivery_qty": pending_delivery_qty,
                        "rate": item.rate,
                        "amount": item.amount,
                    }
                )

    return data
