from ussd.base_menu import Menu
from ussd.requests import Request


class Doctor(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)

    def request_doctor(self):
        text = """
            Received.
            Doctor will get back to you.
        """
        consultation = self.make_request('post', '/consultation-requests')
        return self.ussd_end(text)

    def execute(self):
        try:
            menu = {
                0: self.request_doctor,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))