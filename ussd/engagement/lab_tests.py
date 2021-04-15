from ussd.base_menu import Menu
from ussd.requests import Request


class LabTests(Menu, Request):
    def __init__(self, session_id, session_data, user_option, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option, level)
        Request.__init__(self, base_url)

    def home(self):
        text = "What do yo want to do?\n1. List of Test\n2. Tests with price\n3. Tests without price\n4. Take a Test\n99. Main Menu"

        self.session_data.update({
            "menu": "lab_tests",
            "base": False,
            "level": 1
        })
        return self.ussd_proceed(text)

    def close_session(self):
        text = "Received.\nLaboratory will get back to you."

        return self.ussd_end(text)

    def test_list(self):
        text = "Your test recommendations"
        tests = self.make_request(
            'get',
            f"/labtest?citizen={self.session_data.get('user').get('_id')}")
        for x, y in enumerate(tests['data']):
            text += f"{x+1}. {y['test']}\n"
        if tests['total'] == 0:
            text = "No fulfilled tests.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def accepted_tests(self):
        text = "Your test recommendations"
        tests = self.make_request(
            'get',
            f"/labtest?citizen={self.session_data.get('user').get('_id')}&status=fulfilled"
        )
        for x, y in enumerate(tests['data']):
            text += f"{x+1}. {y['test']}\n"
        if tests['total'] == 0:
            text = "No accepted tests.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def pending_tests(self):
        text = "Your test recommendations"
        tests = self.make_request(
            'get',
            f"/labtest?citizen={self.session_data.get('user').get('_id')}&status=pending"
        )
        for x, y in enumerate(tests['data']):
            text += f"{x+1}. {y['test']}\n"
        if tests['total'] == 0:
            text = "No pending tests.\n"
        text += "00.Back"
        self.session_data['level'] = 0
        return self.ussd_proceed(text)

    def test_type(self):
        text = "Enter test type\n(e.g. malaria test)"

        self.session_data.update({"level": 2})
        return self.ussd_proceed(text)

    def process_test_type(self):
        test_request = self.make_request(
            'POST',
            "/labrequest",
            json={
                'labrequest': {
                    "test": self.user_option,
                    "fulfilled": False,
                    "lab_fulfill": None,
                    "doctor": None,
                    "citizen": self.session_data.get('user').get('_id'),
                    "encounter": None,
                    "lab_dest": self.session_data.get('user').get('pref_laboratory'),
                    "status": "pending",
                    "lab_action": None
                }
            })
        print(test_request)
        return self.close_session()

    def execute(self):
        if self.level == 1:
            self.level = int(self.user_option)
        if self.level == 2:
            self.level = 21
        try:
            menu = {
                0: self.home,
                1: self.test_list,
                2: self.accepted_tests,
                3: self.pending_tests,
                4: self.test_type,
                21: self.process_test_type,
            }
            return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))