import unittest
import frappe
from qontak.qontak.api import QontakApi


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_send_whatsapp_message_outbound_direct(self):
        params = [
            {"key": "1", "value": "otp", "value_text": 300},
            {"key": "2", "value": "expiry", "value_text": "5 menit"},
        ]

        qa_username = frappe.get_value(
            "Qontak Accounts", filters={"default": 1}, fieldname="username"
        )
        template = frappe.get_doc("Alfamind Auth Settings")

        response = QontakApi(
            qa_username=qa_username, message_template_id=template.otp_template
        ).send_whatsapp_message_outbound_direct(
            to_name="Test", to_number="6281901560689", params=params, region="ID"
        )
        print(response)
