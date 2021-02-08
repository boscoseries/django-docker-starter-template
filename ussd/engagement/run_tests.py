from ussd.base_menu import Menu
from ussd.requests import Request


class Tests(Menu, Request):
    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, user,
                      phone_number, level)
        Request.__init__(self, base_url)

    def home(self):
        text = """\
        What do yo want to do?
      1. Check Recommendations
      2. Select Test Type
      99. Main Menu
      """
        self.session_data.update({
            "menu": "run_tests",
            "base": False,
            "level": 1
        })
        return self.ussd_proceed(text)

    def recommendations(self):
        text = """\
            Your test recommendations
        """
        tests = self.make_request('get',
                                  f"/labtest?citizen={self.user['_id']}")
        for x, y in enumerate(tests['data']):
            text += f"{x+1}. {y['test']}\n"
        if tests['total'] == 0:
            text = "No tests recommended.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def test_types(self):
        text = """\
             Select Test Type
             1. Malaria Test
             2. PCV Test
             3. Hepatitis B Test
        """
        self.session_data.update({"level": 3})
        return self.ussd_proceed(text)

    def close_session(self):
        text = """\
            Received.
            Laboratory will get back to you.
        """
        return self.ussd_end(text)

    def execute(self):
        if self.level == 1:
            if self.user_option == '1':
                self.level = 1
            else:
                self.level = 2
        try:
            menu = {
                0: self.home,
                1: self.recommendations,
                2: self.test_types,
                3: self.close_session,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))