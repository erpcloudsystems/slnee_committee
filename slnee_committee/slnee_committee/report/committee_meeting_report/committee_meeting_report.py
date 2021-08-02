# Copyright (c) 2013, erpcloud.systems and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _


def execute(filters=None):
    columns, data = [], []
    columns = get_columns()
    data = get_data(filters, columns)
    return columns, data


def get_columns():
    return [
        {
            "label": _("Meeting"),
            "fieldname": "name",
            "fieldtype": "Link",
            "options": "Committee Meeting",
            "width": 120
        },
        {
            "label": _("State 1"),
            "fieldname": "workflow_state_1",
            "fieldtype": "Data",
            "width": 140
        },
		{
			"label": _("State 2"),
			"fieldname": "workflow_state_2",
			"fieldtype": "Data",
			"width": 140
		}
    ]


def get_data(filters, columns):
    item_price_qty_data = []
    item_price_qty_data = get_item_price_qty_data(filters)
    return item_price_qty_data


def get_item_price_qty_data(filters):
    conditions = ""
    item_results = frappe.db.sql("""
				SELECT
						`tabCommittee Meeting`.name as name,

						(SELECT `tabRequests Table`.action_taken
						FROM `tabRequests Table`
						WHERE `tabRequests Table`.parent = `tabCommittee Meeting`.name
						and `tabRequests Table`.action_taken IS NULL) as workflow_state_1,

						(SELECT `tabRequests Table`.action_taken
						FROM `tabRequests Table`
						WHERE `tabRequests Table`.parent = `tabCommittee Meeting`.name
						and `tabRequests Table`.action_taken IS NOT NULL) as workflow_state_2


				FROM
				`tabCommittee Meeting` join `tabRequests Table`
				
				ON
				`tabRequests Table`.parent = `tabCommittee Meeting`.name

				WHERE
				`tabCommittee Meeting`.docstatus == 1
				{conditions}

				""".format(conditions=conditions), filters, as_dict=1)

    # price_list_names = list(set([item.price_list_name for item in item_results]))

    # buying_price_map = get_price_map(price_list_names, buying=1)
    # selling_price_map = get_price_map(price_list_names, selling=1)

    result = []
    if item_results:
        for item_dict in item_results:
            data = {
                'name': item_dict.name,
                'workflow_state_1': item_dict.workflow_state_1,
                'workflow_state_2': item_dict.workflow_state_2,
            }
            result.append(data)

    return result


def get_price_map(price_list_names, buying=0, selling=0):
    price_map = {}

    if not price_list_names:
        return price_map

    rate_key = "Buying Rate" if buying else "Selling Rate"
    price_list_key = "Buying Price List" if buying else "Selling Price List"

    filters = {"name": ("in", price_list_names)}
    if buying:
        filters["buying"] = 1
    else:
        filters["selling"] = 1

    pricing_details = frappe.get_all("Item Price",
                                     fields=["name", "price_list", "price_list_rate"], filters=filters)

    for d in pricing_details:
        name = d["name"]
        price_map[name] = {
            price_list_key: d["price_list"],
            rate_key: d["price_list_rate"]
        }

    return price_map
