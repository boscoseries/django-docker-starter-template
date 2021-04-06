from django.http import HttpResponse
from django.core.cache import cache


class Menu(object):
    def __init__(self,
                 session_id,
                 session_data,
                 user_option,
                 user,
                 phone_number=None,
                 level=None):
        self.session_data = session_data
        self.session_id = session_id
        self.user = user
        self.user_option = user_option
        self.phone_number = phone_number
        self.level = level
        
        print('''

              Entered start Menu

              ''')

    def error(self):
        raise NotImplementedError

    def ussd_proceed(self, text):
        cache.set(self.session_id, self.session_data)
        cache.set('user', self.user)
        text = "CON {}".format(text)
        return HttpResponse(text, content_type="text/plain")

    def ussd_end(self, text):
        cache.delete(self.session_id)
        text = "END {}".format(text)
        return HttpResponse(text, content_type="text/plain")

    def home(self):
        """serves the home menu"""
        text = """\
        Welcome to Oyo State Tele-medicine Service
        1. Register
        2. Exit
        """
        return self.ussd_proceed(text)

    def start(self):
        """serves the home menu for returning users"""
        text = """\
            Welcome {}, what would you like to do today?
            1. Chat with a Doctor
            2. Check my Drugs
            3. Check Tests
            4. Contact Hospital
            5. Request Health Taxi
        """.format(self.user['firstName'])
        return self.ussd_proceed(text)
