import frappe
from frappe.utils import flt
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters)
    return columns, data


def get_columns():
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
    filters = [
        ["Sales Invoice", "company", "=", report_filters.get("company")],
        ["Sales Invoice", "posting_date", "<=", report_filters.get("posting_date")],
        ["Sales Invoice", "docstatus", "=", 1],
    ]

    if report_filters.get("sales_invoice"):
        filters.append(
            ["Sales Invoice", "name", "=", report_filters.get("sales_invoice")]
        )

    return filters


def get_data(filters):
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
