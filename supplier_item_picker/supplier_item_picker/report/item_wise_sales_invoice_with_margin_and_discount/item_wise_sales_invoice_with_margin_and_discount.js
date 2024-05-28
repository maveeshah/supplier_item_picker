// Copyright (c) 2024, Ameer Muavia Shah and contributors
// For license information, please see license.txt

// Copyright (c) 2024, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.query_reports["Item-wise Sales Invoice with Margin and Discount"] = {
	filters: [
		{
			label: __("Customer"),
			fieldname: "customer",
			fieldtype: "Link",
			options: "Customer",
		},
		{
			label: __("Customer Group"),
			fieldname: "customer_group",
			fieldtype: "Link",
			options: "Customer Group",
		},
		{
			label: __("Mode of Payment"),
			fieldname: "mode_of_payment",
			fieldtype: "Link",
			options: "Mode of Payment",
		},
		{
			label: __("Owner"),
			fieldname: "owner",
			fieldtype: "Link",
			options: "User",
		},
		{
			label: __("Cost Center"),
			fieldname: "cost_center",
			fieldtype: "Link",
			options: "Cost Center",
		},
		{
			label: __("Warehouse"),
			fieldname: "warehouse",
			fieldtype: "Link",
			options: "Warehouse",
		},
		{
			label: __("Brand"),
			fieldname: "brand",
			fieldtype: "Link",
			options: "Brand",
		},
		{
			label: __("Item Group"),
			fieldname: "item_group",
			fieldtype: "Link",
			options: "Item Group",
		},
	],
};
