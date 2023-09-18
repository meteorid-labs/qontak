import requests
import frappe
from qontak.utils.whatsapp import whatsapp_phone_number
import json


class QontakApi():
    def __init__(self, qa_username, message_template_id):
        qontak_account = frappe.get_doc("Qontak Accounts", qa_username)
        self.qa = qontak_account
        self.message_template_id = message_template_id

        qontak_settings = frappe.get_doc("Qontak Settings")
        self.base_url = qontak_settings.base_api_url or "https://service-chat.qontak.com"

        self.access_token = None
        self.headers = {"Content-Type": "application/json"}

        self.get_access_token()

    def setup_template(self):
        self.message_template_id = self.qontak_template.message_template_id

    def get_access_token(self):
        if not self.access_token:
            url = self.base_url + '/oauth/token'

            payload = {
                "username": self.qa.username,
                "password": self.qa.get_password(
                    fieldname="password", raise_exception=False),
                "grant_type": "password",
                "client_id": self.qa.client_id,
                "client_secret": self.qa.get_password(
                    fieldname="client_secret", raise_exception=False)
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

    def send_whatsapp_message_outbound_direct(self, to_name=None, to_number=None, params=None, region=None, source=None):
        url = self.base_url + "/api/open/v1/broadcasts/whatsapp/direct"

        payload = {
            "to_number": whatsapp_phone_number(to_number, region),
            "to_name": to_name,
            "message_template_id": self.message_template_id,
            "channel_integration_id": self.qa.channel_integration_id,
            "language": {"code": "id"},
            "parameters": {
                "body": params
            }
        }

        response = requests.request(
            "POST", url, json=payload, headers=self.headers)

        _create_qontak_request(
            payload=payload, response=response, source=source)

        return response.json()


def _create_qontak_request(**kwargs):
    from frappe.utils.background_jobs import enqueue
    enqueue(
        _start_store_qontak_request,
        queue="default",
        timeout=10000,
        event="qontak_request",
        job_name="Qontak Request - {}".format(kwargs["source"]),
        **kwargs,
        now=frappe.conf.developer_mode or frappe.flags.in_test,
    )


def _start_store_qontak_request(payload=None, response=None, source=None):
    response_raw = None

    try:
        response_raw = response.json()
    except:
        response_raw = response.text if response else []

    qontak_request = frappe.new_doc("Qontak Requests")
    qontak_request.update({
        "to_name": payload.get("to_name") if payload else "",
        "to_number": payload.get("to_number") if payload else "",
        "source": source,
        "request": json.dumps(payload) if payload else [],
        "response": json.dumps(response_raw),
        "status_code": response.status_code,
        "status": "Success" if response.ok else "Failed",
    })
    qontak_request.insert(ignore_permissions=True)
    frappe.db.commit()
