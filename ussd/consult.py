from .base_menu import Menu
from .requests import Request


class Consultation(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)
