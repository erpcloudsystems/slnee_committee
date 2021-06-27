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
	pass
	def on_update_after_submit(self):
		self.update_request()

	def update_request(self):
		for value in self.requests_table:
			frappe.db.sql("""update `tabCommunication With Committee` set workflow_state = %s where	name=%s """, (value.action_taken, value.request_no))
			#return q1