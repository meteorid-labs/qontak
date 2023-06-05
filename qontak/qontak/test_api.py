import unittest
import frappe
from qontak.qontak.api import QontakApi


class TestApi(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pass

    def test_send_whatsapp_message_outbound_direct(self):
        params = [
            {
                "key": "1",
                "value": "otp",
                "value_text": 300
            },
            {
                "key": "2",
                "value": "expiry",
                "value_text": "5 menit"
            }
        ]

        response = QontakApi().send_whatsapp_message_outbound_direct(
            "Aslam", "6281901560689", params, "ID")
        print(response)
