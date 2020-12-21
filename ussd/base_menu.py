import json

# from flask import make_response, current_app
from django.http import HttpResponse

# from ..database import redisfrom
from django.core.cache import cache

class Menu(object):
    def __init__(self, session_id, session, user, user_option, phone=None, level=None):
        self.session = session
        self.session_id = session_id
        self.user = user
        self.user_option = user_option
        self.phone = phone
        self.level = level

    def execute(self):
        raise NotImplementedError

    def ussd_proceed(self, menu_text):
        cache.set(self.session_id, self.session)
        menu_text = "CON {}".format(menu_text)
        return HttpResponse(menu_text, content_type="text/plain")

    def ussd_end(self, menu_text):
        cache.delete(self.session_id)
        menu_text = "END {}".format(menu_text)
        return HttpResponse(menu_text, content_type="text/plain")

    def home(self):
        """serves the home menu"""
        menu_text = """
        Welcome to Oyo State Tele-medicine Service
        1. Register
        2. Exit
        """
        self.session['level'] = 1
        return self.ussd_proceed(menu_text)
