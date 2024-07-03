# Copyright (c) 2024, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []

    # Add columns to the report
    columns = get_columns()

    # Fetch data based on filters
    data = get_data(filters)

    return columns, data


def get_columns():
    return [
        {
            "label": _("Item"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 175,
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 175,
        },
        {
            "label": _("Item Group"),
            "fieldname": "item_group",
            "fieldtype": "Link",
            "options": "Item Group",
            "width": 175,
        },
        {
            "label": _("Brand"),
            "fieldname": "brand",
            "fieldtype": "Link",
            "options": "Brand",
            "width": 175,
        },
        {
            "label": _("Display Warehouse"),
            "fieldname": "display_warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 175,
        },
        {
            "label": _("Storage Warehouse"),
            "fieldname": "storage_warehouse",
            "fieldtype": "Link",
            "options": "Warehouse",
            "width": 175,
        },
        {
            "label": _("Display Qty"),
            "fieldname": "display_qty",
            "fieldtype": "Float",
            "width": 150,
        },
        {
            "label": _("Storage Qty"),
            "fieldname": "storage_qty",
            "fieldtype": "Float",
            "width": 150,
        },
    ]


def get_data(filters):
    conditions, values = get_conditions(filters)

    query = f"""
        SELECT 
            sle.item_code,
            i.item_name,
            i.item_group,
            i.brand,
            sle.warehouse as display_warehouse,
            sle.warehouse as storage_warehouse,
            sle.actual_qty as display_qty,
            sle.actual_qty as storage_qty
            FROM 
            `tabStock Ledger Entry` sle
        JOIN
            `tabItem` i ON sle.item_code = i.name
        WHERE
            sle.name is not null
            {conditions}
        GROUP BY 
            sle.item_code, sle.warehouse
    """

    data = frappe.db.sql(query, values, as_dict=True)

    return data


def get_conditions(filters):
    conditions = ""
    values = {"start_date": filters.start_date, "end_date": filters.end_date}

    if filters.get("company"):
        conditions += " AND sle.company = %(company)s"
        values["company"] = filters.company
    if filters.get("item_group"):
        conditions += " AND i.item_group = %(item_group)s"
        values["item_group"] = filters.item_group
    if filters.get("brand"):
        conditions += " AND i.brand = %(brand)s"
        values["brand"] = filters.brand
    if filters.get("item"):
        conditions += " AND i.name = %(item)s"
        values["item"] = filters.item
    if filters.get("from_date") and filters.get("to_date"):
        conditions += " AND sle.posting_date BETWEEN %(from_date)s AND %(to_date)s"
        values["from_date"] = filters.from_date
        values["to_date"] = filters.to_date

    return conditions, values
