import requests
import frappe


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
        qs = frappe.get_doc("Qontak Settings", "Qontak Settings")

        # if one of the value is None, raise error
        if not all([qs.username, qs.password, qs.client_id, qs.client_secret]):
            frappe.throw('Please set Qontak Settings first')

        self.username = qs.username
        self.password = qs.get_password(
            fieldname="password", raise_exception=False)
        self.client_id = qs.client_id
        self.client_secret = qs.get_password(
            fieldname="client_secret", raise_exception=False)
        self.message_template_id = qs.message_template_id
        self.channel_integration_id = qs.channel_integration_id

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

    def send_whatsapp_message_outbound_direct(self):
        url = "https://service-chat.qontak.com/api/open/v1/broadcasts/whatsapp/direct"

        payload = {
            "to_number": "6281901560689",
            "to_name": "Aslam",
            "message_template_id": self.message_template_id,
            "channel_integration_id": self.channel_integration_id,
            "language": {"code": "id"},
            "parameters": {"body": [
                {
                    "key": "1",
                    "value": "otp",
                    "value_text": "085657"
                }
            ]}
        }

        response = requests.request(
            "POST", url, json=payload, headers=self.headers)

        print(response.text)
