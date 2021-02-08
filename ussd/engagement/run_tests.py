from ussd.base_menu import Menu
from ussd.requests import Request


class Tests(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)
        if self.level:
            self.level = int(self.user_option)

    def home(self):
        # print('-------->HOME', self.session_data)
        text = """\
        What do yo want to do?
      1. Check Prescription
      2. Fulfilled Prescription
      3. Unavailable Prescription
      99. Main Menu
      """
        self.session_data.update({
            "menu": "prescription",
            "base": False,
            "level": 1
        })
        return self.ussd_proceed(text)

    def all_prescription(self):
        # self.user['_id'] = "6000e703539178242498c54b"
        body = """\
            All your Prescription:
        """
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}")
        for x, y in enumerate(prescription['data']):
            body += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            body = "\nYou have no prescription.\n"

        text = """\
            {}
            00. Back
        """.format(body)
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def fulfilled_prescription(self):
        # self.user['_id'] = "6000e703539178242498c54b"
        body = """\
            Available at your Pharmacy
        """
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}&fulfilled=true")
        for x, y in enumerate(prescription['data']):
            body += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            body = "\nYou have no prescription.\n"

        text = """\
            {}
            00. Back
        """.format(body)
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def unavailable_prescription(self):
        # self.user['_id'] = "6000e703539178242498c54b"
        body = """\
             Un-available at your Pharmacy
        """
        print(self.user["_id"])
        prescription = self.make_request(
            'get', f"/medication?citizen={self.user['_id']}&fulfilled=false")
        for x, y in enumerate(prescription['data']):
            body += f"{x+1}. {y['medication']}\n"
        if prescription['total'] == 0:
            body += "\nYou have no prescription.\n"

        text = """\
            {}
            00. Back
        """.format(body)
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def close_session(self):
        print('entered close session')
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