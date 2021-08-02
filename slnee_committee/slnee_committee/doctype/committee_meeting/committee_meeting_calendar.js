// Copyright (c) 2015, Frappe Technologies Pvt. Ltd. and Contributors
// License: GNU General Public License v3. See license.txt

frappe.views.calendar['Committee Meeting'] = {
    field_map: {
        start: 'start',
        end: 'end',
        id: 'name',
        title: 'subject',
        status: 'status',
        allDay: "all_day",
        color: 'color'
    },
    order_by: 'end',
    get_events_method: 'slnee_committee.slnee_committee.doctype.committee_meeting.committee_meeting.calendar_view'
}