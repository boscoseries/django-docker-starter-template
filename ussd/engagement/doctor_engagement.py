from ussd.base_menu import Menu
from ussd.requests import Request


class Doctor(Menu, Request):
    def __init__(self, session_id, session_data, user_option, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, level)
        Request.__init__(self, base_url)

    def close_session(self):
        text = "Received.\nDoctor will get back to you."

        engage_doctor = self.make_request(
            'post',
            '/consultation-requests',
            data={"citizen": self.session_data.get("user").get('_id')})
        print(engage_doctor)
        return self.ussd_end(text)

    def execute(self):
        try:
            menu = {
                0: self.close_session,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))