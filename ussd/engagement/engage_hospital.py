from ussd.base_menu import Menu
from ussd.requests import Request


class Hospital(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)

    def doctor_close_session(self):
        text = """\
            Received.
            Doctor will get back to you.
        """
        return self.ussd_end(text)

    def end_session(self):
        text = """\
            Goodbye
        """
        return self.ussd_end(text)

    def home(self):
        text = """\
            Select a service
            1. Contact Hospital Doctor
            2. Contact Hospital Pharmacy
            3. Contact Hospital Lab
            99. Main Menu
        """
        self.session_data.update({
            "menu": "engage_hospital",
            "base": False,
            "level": 1,
        })
        return self.ussd_proceed(text)

    def engage_doctor(self):
        # hospital_option = self.session_data['hospital_dict'][self.user_option]
        text_unavailable = """
        Doctor is not available at your preferred hospital,
        would you like to engage another hospital?
        1. Yes
        2. No
        """
        text = """\
            Available at your Pharmacy:
        """
        doctor = self.make_request('get', f"/doctor?availability=true")
        print(doctor)
        if doctor['total'] == 0:
            self.session_data.update({"level": 101})
            return self.ussd_proceed(text_unavailable)
        return self.doctor_close_session()

    def engage_pharmacy(self):
        text = """\
            Received.
            Pharmacy will get back to you.
        """
        return self.ussd_end(text)

    def engage_laboratory(self):
        text = """\
            Received.
            Laboratory will get back to you.
        """
        return self.ussd_end(text)

    def execute(self):
        if self.level == 1:
            self.level = int(self.user_option)
        if self.level == 101:
            if self.user_option == '1':
                self.level = 1
            if self.user_option == '2':
                self.level = 4
        try:
            menu = {
                0: self.home,
                1: self.engage_doctor,
                2: self.engage_pharmacy,
                3: self.engage_laboratory,
                4: self.end_session,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))