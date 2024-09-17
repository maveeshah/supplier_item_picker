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
    columns = [
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
        }
    ]
    
    warehouses = get_warehouses()

    for warehouse in warehouses:
        columns.append({
            "label": _(f"{warehouse} Qty"),
            "fieldname": frappe.scrub(f"{warehouse}_qty"),
            "fieldtype": "Float",
            "width": 150,
        })
    
    return columns


def get_data(filters):
    conditions, values = get_conditions(filters)
    
    # Fetch all warehouses
    warehouses = get_warehouses()
    
    # Create a dynamic SQL query to pivot the data
    select_statements = []
    for warehouse in warehouses:
        select_statements.append(f"""
            SUM(CASE WHEN sle.warehouse = '{warehouse}' THEN sle.actual_qty ELSE 0 END) AS `{frappe.scrub(warehouse)}_qty`
        """)
    
    query = f"""
        SELECT 
            sle.item_code,
            i.item_name,
            i.item_group,
            i.brand,
            {', '.join(select_statements)}
        FROM 
            `tabStock Ledger Entry` sle
        JOIN
            `tabItem` i ON sle.item_code = i.name
        WHERE
            sle.docstatus = 1

            {conditions}
        GROUP BY 
            sle.item_code
    """

    data = frappe.db.sql(query, values, as_dict=True)

    return data


def get_warehouses():
    warehouses = frappe.db.sql("""
        SELECT DISTINCT warehouse FROM `tabStock Ledger Entry`
    """, as_dict=True)
    
    return [w['warehouse'] for w in warehouses]

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
