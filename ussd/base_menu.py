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
              Entered Base Menu
              ''')

    def error(self):
        raise NotImplementedError

    def ussd_proceed(self, text):
        cache.set(self.session_id, self.session_data)
        cache.set('user', self.user)
        text = "CON {}".format(text)
        print('text with CON----------------->', text)
        return HttpResponse(text, content_type="text/plain")

    def ussd_end(self, text):
        cache.delete(self.session_id)
        text = "END {}".format(text)
        return HttpResponse(text, content_type="text/plain")

    def home(self):
        """serves the home menu for new users"""
        text = """\
        Welcome to Oyo State Tele-medicine Service
        1. Register
        2. Exit
        """
        return self.ussd_proceed(text)

    def start(self):
        """serves the home menu for returning users"""
        text = "Welcome {}, what would you like to do today?\n1. Chat with a Doctor\n2. Check my Drugs\n3. Check Tests\n4. Contact Hospital\n5. Request Health Taxi".format(
            self.user.get('firstName'))
        print('text without CON ------------>', text)
        return self.ussd_proceed(text)
