# Copyright (c) 2023, Meteor Inovasi Digital and Contributors
# See license.txt

import frappe
from frappe.tests.utils import FrappeTestCase


class TestQontakSettings(FrappeTestCase):
    def test_can_get_qontak_setting(self):
        qos = frappe.get_doc("Qontak Settings", "Qontak Settings")
        self.assertIsNotNone(qos.qontak_account)

    def test_api(self):
        from qontak.qontak.api import QontakApi
        params = [
            {
                "key": "1",
                "value": "otp",
                "value_text": "123456"
            },
            {
                "key": "2",
                "value": "expiry",
                "value_text": "5 minutes"
            }
        ]

        res = QontakApi().send_whatsapp_message_outbound_direct(
            "Aslam", "+6281901560689", params, "ID")

        self.assertEqual(res["status"], "success")
