from ussd.base_menu import Menu
from ussd.requests import Request


class Prescribe(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)
        if self.level:
            self.level = int(self.user_option)

    def home(self):
        text = """\
        What do yo want to do?
      1. Medication List
      2. Fulfilled Prescription
      3. Un-fulfilled Prescription
      99. Main Menu
      """
        self.session_data.update({
            "menu": "prescription",
            "base": False,
            "level": 1
        })
        return self.ussd_proceed(text)

    def all_prescription(self):
        text = """\
            All your Prescription:
        """
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text = "\nYou have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def fulfilled_prescription(self):
        text = """\
            Available at your Pharmacy
        """
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}&fulfilled=true")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text = "\nYou have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def unavailable_prescription(self):
        text = """\
             Un-available at your Pharmacy
        """
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}&fulfilled=false")
        for x, y in enumerate(prescription['data']):
            text += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            text += "\nYou have no prescription.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def close_session(self):
        text = """\
            Received.
            Pharmacy will get back to you.
        """
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
            return self.ussd_end(str(e))