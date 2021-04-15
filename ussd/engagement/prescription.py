from ussd.base_menu import Menu
from ussd.requests import Request
from sentry_sdk import capture_exception
from django.core.cache import cache


class Prescribe(Menu, Request):
    def __init__(self, session_id, session_data, user_option, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, level)
        Request.__init__(self, base_url)
        if self.level:
            self.level = int(self.user_option)

    def home(self):
        text = "What do yo want to do?\n 1. List of Drugs\n2. Drugs with price\n3. Drugs without price\n99. Main Menu"

        self.session_data.update({
            "menu": "prescription",
            "base": False,
            "level": 1
        })
        return self.ussd_proceed(text)

    def all_prescription(self):
        text = "All your Prescription:\n"

        prescription = self.make_request(
            'get', f"/medication?citizen={self.session_data.get('user').get('_id')}")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text = "You have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def fulfilled_prescription(self):
        text = "Available at your Pharmacy"

        prescription = self.make_request(
            'get', f"/medication?citizen={self.session_data.get('user').get('_id')}&fulfilled=true")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text = "You have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def unavailable_prescription(self):
        text = "Un-available at your Pharmacy"

        prescription = self.make_request(
            'get', f"/medication?citizen={self.session_data.get('user').get('_id')}&fulfilled=false")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text = "You have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def close_session(self):
        text = "Received.\nPharmacy will get back to you."

        return self.ussd_end(text)

    def execute(self):
        try:
            menu = {
                0: self.home,
                1: self.all_prescription,
                2: self.fulfilled_prescription,
                3: self.unavailable_prescription,
            }
            return menu.get(self.level)()
        except Exception as e:
            cache.delete(self.session_id)
            capture_exception(e)
            return self.ussd_end("Something went wrong!")