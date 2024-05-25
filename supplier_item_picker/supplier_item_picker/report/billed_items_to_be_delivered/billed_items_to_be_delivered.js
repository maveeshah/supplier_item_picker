// Copyright (c) 2024, Ameer Muavia Shah and contributors
// For license information, please see license.txt

frappe.query_reports["Billed Items To Be Delivered"] = {

	filters: [
		{
			label: __("Company"),
			fieldname: "company",
			fieldtype: "Link",
			options: "Company",
			reqd: 1,
			default: frappe.defaults.get_default("Company"),
		},
		{
			label: __("As on Date"),
			fieldname: "posting_date",
			fieldtype: "Date",
			reqd: 1,
			default: frappe.datetime.get_today(),
		},
		{
			label: __("Sales Invoice"),
			fieldname: "sales_invoice",
			fieldtype: "Link",
			options: "Sales Invoice",
		},
	],
};
