# Copyright (c) 2023, Meteor Inovasi Digital and contributors
# For license information, please see license.txt

import frappe
from frappe.model.document import Document


class QontakAccounts(Document):
    def autoname(self):
        self.name = self.username

    def before_validate(self):
        self.there_must_be_only_one_default()

    def there_must_be_only_one_default(self):
        qa = frappe.get_all("Qontak Accounts", filters={"default": 1})
        if self.default == 1:
            for account in qa:
                if account.name == self.name:
                    continue
                account = frappe.get_doc("Qontak Accounts", account.name)
                account.set("default", 0)
                account.save()
        if not qa and self.default == 0:
            self.default = 1
