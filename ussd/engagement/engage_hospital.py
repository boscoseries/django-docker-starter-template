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
            1. Doctor
            2. Pharmacy
            3. Laboratory
            99. Main Menu
        """
        self.session_data.update({
            "menu": "engage_hospital",
            "base": False,
            "level": 1,
        })
        return self.ussd_proceed(text)

    def hospital_choices(self):
        pref_hospital = """\
        Choose your preferred hospital
        """
        body = """\
        """
        hospital_dict = {}
        hospitals = self.make_request('get', '/hospital')
        n = 1
        for x, y in enumerate(hospitals['data']):
            n += 1
            if y['_id'] == self.user['pref_hospital']:
                pref_hospital += f"1. {y['name']}\n"
                hospital_dict['1'] = y['_id']
            else:
                body += f"{n}. {y['name']}\n"
                hospital_dict[str(n)] = y['_id']
        text = pref_hospital + body

        self.session_data.update({
            "level": 2,
            "hospital_dict": hospital_dict,
            "service_choice": self.user_option
        })
        return self.ussd_proceed(text)

    def engage_doctor(self):
        hospital_option = self.session_data['hospital_dict'][self.user_option]
        text_unavailable = """
        Doctor is not available at your preferred Hospital,
        would you like to engage another hospital?
        1. Yes
        2. No
        """
        text = """\
            Available at your Pharmacy:
        """
        doctor = self.make_request(
            'get', f"/doctor?availability=false&hospital={hospital_option}")
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
        if self.level == 2:
            if self.session_data.get('service_choice') == '1':
                self.level = 2
            elif self.session_data.get('service_choice') == '2':
                self.level = 3
            else:
                self.level = 4
        if self.level == 101:
            if self.user_option == '1':
                self.level = 1
            else:
                self.level = 5
        try:
            menu = {
                0: self.home,
                1: self.hospital_choices,
                2: self.engage_doctor,
                3: self.engage_pharmacy,
                4: self.engage_laboratory,
                5: self.end_session,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))