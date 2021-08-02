from __future__ import unicode_literals
import frappe
from frappe import _
from six import iteritems
from email_reply_parser import EmailReplyParser
from frappe.utils import (flt, getdate, get_url, now,
	nowtime, get_time, today, get_datetime, add_days)
from erpnext.controllers.queries import get_filters_cond
from frappe.desk.reportview import get_match_cond
from erpnext.hr.doctype.daily_work_summary.daily_work_summary import get_users_email
from erpnext.hr.doctype.holiday_list.holiday_list import is_holiday
from frappe.model.document import Document
from erpnext.education.doctype.student_attendance.student_attendance import get_holiday_list
from frappe.model.document import Document
# import frappe

class CommitteeMeeting(Document):

	@frappe.whitelist()
	def on_submit(self):
		self.update_request()

	@frappe.whitelist()
	def on_update_after_submit(self):
		self.update_request()

	@frappe.whitelist()
	def update_request(self):
		for value in self.requests_table:
			frappe.db.sql("""update `tabCommunication With Committee` set workflow_state = %s where	name=%s """, (value.action_taken, value.request_no))

	@frappe.whitelist()
	def get_requests(self):
		requests = frappe.db.sql(""" select name, posting_date, request_type, request_description, committee from `tabCommunication With Committee` where workflow_state = 'Escalated To Committee' or workflow_state = 'Resent To Committee'""",as_dict=1)
		for x in requests:
			y = self.append("requests_table", {})
			y.request_no = x.name
			y.request_date = x.posting_date
			y.request_type = x.request_type
			y.request_description = x.request_description
			y.committee = x.committee


	@frappe.whitelist()
	def get_members(self):
			members = frappe.db.sql(
				""" select DISTINCT member, member_type, employee_code, name1, entity_name, email, role_level 
				 from `tabCommittee Members` join `tabRequests Table` on `tabCommittee Members`.parent = `tabRequests Table`.committee
				 join  `tabCommittee Meeting` on `tabCommittee Meeting`.name = `tabRequests Table`.parent
				  where `tabCommittee Meeting`.name = %s GROUP BY member""",self.name,as_dict=1)

			result = {}

			for x in members:
				if x.member not in self.committee_members:
					result = {
						'member': x.member,
						'member_type': x.member_type,
						'employee_code': x.employee_code,
						'name1': x.name1,
						'email': x.email,
						'role_level': x.role_level,
						'entity_name': x.entity_name
					}
					self.append("committee_members", result)
					frappe.db.commit()

@frappe.whitelist()
def calendar_view(start, end):
	if not frappe.has_permission("Shows", "read"):
		raise frappe.PermissionError

	return frappe.db.sql("""select
				timestamp(`meeting_date`, meeting_time) as start,
				timestamp(`meeting_date`, meeting_time) as end,
				name,
				color,
				CONCAT_WS(' - ',subject,meeting_location) as subject,
				meeting_status as status

		from `tabCommittee Meeting`
		where `docstatus` = 1
		and `meeting_date` between %(start)s and %(end)s""", {
		"start": start,
		"end": end
	}, as_dict=True)



	pass