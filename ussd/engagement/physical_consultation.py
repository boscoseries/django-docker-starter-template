from ussd.base_menu import Menu
from ussd.requests import Request


class Consult(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)

    def close_session(self):
        text = """\
        Received.
        Doctor will get back to you.
        """
        return self.ussd_end(text)

    def execute(self):
        try:
            menu = {
                0: self.close_session,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))