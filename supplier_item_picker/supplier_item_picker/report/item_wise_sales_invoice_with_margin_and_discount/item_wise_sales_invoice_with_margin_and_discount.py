# Copyright (c) 2024, Ameer Muavia Shah and contributors
# For license information, please see license.txt

import frappe
from frappe import _


def execute(filters=None):
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
            "width": 150,
        },
        {
            "label": _("Customer"),
            "fieldname": "customer",
            "fieldtype": "Link",
            "options": "Customer",
            "width": 150,
        },
        {
            "label": _("Posting Date"),
            "fieldname": "posting_date",
            "fieldtype": "Date",
            "width": 100,
        },
        {
            "label": _("Item Code"),
            "fieldname": "item_code",
            "fieldtype": "Link",
            "options": "Item",
            "width": 100,
        },
        {
            "label": _("Item Name"),
            "fieldname": "item_name",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Qty"),
            "fieldname": "qty",
            "fieldtype": "Float",
            "width": 100,
        },
        {
            "label": _("UOM"),
            "fieldname": "uom",
            "fieldtype": "Link",
            "options": "UOM",
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
            "width": 100,
        },
        {
            "label": _("Margin Type"),
            "fieldname": "margin_type",
            "fieldtype": "Data",
            "width": 100,
        },
        {
            "label": _("Margin Rate or Amount"),
            "fieldname": "margin_rate_or_amount",
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "label": _("Rate with Margin"),
            "fieldname": "rate_with_margin",
            "fieldtype": "Currency",
            "width": 100,
        },
        {
            "label": _("Discount (%) on Price List with Margin"),
            "fieldname": "discount_percentage",
            "fieldtype": "Percent",
            "width": 100,
        },
        {
            "label": _("Discount Amount"),
            "fieldname": "discount_amount",
            "fieldtype": "Currency",
            "width": 100,
        },
    ]


def get_data(filters):
    conditions = get_conditions(filters)
    query = """
        SELECT 
            si.name as sales_invoice, 
            si.customer, 
            si.posting_date, 
            sii.item_code, 
            sii.item_name, 
            sii.qty, 
            sii.uom, 
            sii.rate, 
            sii.amount, 
            sii.margin_type, 
            sii.margin_rate_or_amount, 
            sii.rate_with_margin, 
            sii.discount_percentage, 
            sii.discount_amount 
        FROM 
            `tabSales Invoice` si 
        INNER JOIN 
            `tabSales Invoice Item` sii 
        ON 
            si.name = sii.parent
        LEFT JOIN
            `tabSales Invoice Payment` sip
        ON
            si.name = sip.parent
        WHERE 
            si.docstatus = 1
            AND (sii.margin_rate_or_amount > 0 OR sii.discount_amount > 0)
            {conditions}
        ORDER BY 
            si.posting_date DESC
    """.format(
        conditions=conditions
    )

    data = frappe.db.sql(query, filters, as_dict=1)
    return data


def get_conditions(filters):
    conditions = ""
    if filters.get("customer"):
        conditions += " AND si.customer = %(customer)s"
    if filters.get("customer_group"):
        conditions += " AND si.customer_group = %(customer_group)s"
    if filters.get("mode_of_payment"):
        conditions += " AND sip.mode_of_payment = %(mode_of_payment)s"
    if filters.get("owner"):
        conditions += " AND si.owner = %(owner)s"
    if filters.get("cost_center"):
        conditions += " AND sii.cost_center = %(cost_center)s"
    if filters.get("warehouse"):
        conditions += " AND sii.warehouse = %(warehouse)s"
    if filters.get("brand"):
        conditions += " AND sii.brand = %(brand)s"
    if filters.get("item_group"):
        conditions += " AND sii.item_group = %(item_group)s"

    return conditions
