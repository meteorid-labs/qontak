import requests
import frappe
from qontak.utils.whatsapp import whatsapp_phone_number


class QontakApi():
    def __init__(self):
        self.base_url = "https://service-chat.qontak.com"
        self.access_token = None
        self.headers = {
            "Content-Type": "application/json",
        }

        self.setup_credentials()
        self.get_access_token()

    def setup_credentials(self):
        qos = frappe.get_doc("Qontak Settings", "Qontak Settings")

        if not qos.qontak_account:
            frappe.throw('Please set Qontak Settings first')

        qoa = frappe.get_doc("Qontak Accounts", qos.qontak_account)

        # if one of the value is None, raise error
        if not all([
            qoa.username,
            qoa.password,
            qoa.client_id,
            qoa.client_secret,
            qoa.message_template_id,
            qoa.channel_integration_id
        ]):
            frappe.throw('Add Qontak Account before using Qontak API')

        self.username = qoa.username
        self.password = qoa.get_password(
            fieldname="password", raise_exception=False)
        self.client_id = qoa.client_id
        self.client_secret = qoa.get_password(
            fieldname="client_secret", raise_exception=False)
        self.message_template_id = qoa.message_template_id
        self.channel_integration_id = qoa.channel_integration_id

    def get_access_token(self):
        if self.access_token is None:
            url = self.base_url + '/oauth/token'

            payload = {
                "username": self.username,
                "password": self.password,
                "grant_type": "password",
                "client_id": self.client_id,
                "client_secret": self.client_secret
            }

            response = requests.request(
                "POST", url, json=payload, headers=self.headers)

            if response.ok:
                data = response.json()
                self.access_token = data.get('access_token')

                auth_header = {
                    "Authorization": f"Bearer {self.access_token}",
                }

                self.headers.update(auth_header)

    def send_whatsapp_message_outbound_direct(self, to_name=None, to_number=None, params=None, region=None):
        url = self.base_url + "/api/open/v1/broadcasts/whatsapp/direct"

        payload = {
            "to_number": whatsapp_phone_number(to_number, region),
            "to_name": to_name,
            "message_template_id": self.message_template_id,
            "channel_integration_id": self.channel_integration_id,
            "language": {"code": "id"},
            "parameters": {
                "body": params
            }
        }

        response = requests.request(
            "POST", url, json=payload, headers=self.headers)
        # response.raise_for_status()

        return response.json()
