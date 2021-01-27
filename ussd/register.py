import re
import datetime
from .base_menu import Menu
from django.core.cache import cache
from .requests import Request

lga = {
    'A': ["Afijio", "Atiba", "Atisbo", "Akinyele"],
    "Iba": [
        "Ibadan North", "Ibadan North East", "Ibadan North West",
        "Ibadan South East", "Ibadan South West", "Ibarapa North",
        "Ibarapa East", "Ibarapa Central"
    ],
    "K, L, E": ["Kajola", "Lagelu", "Egbeda"],
    "It, Is, Iw, Id, Ir": ["Itesiwaju", "Iwajowa", "Iseyin", "Ido", "Irepo"],
    "Og": ["Ogbomosho South", "Ogbomosho North", "Ogo Oluwa"],
    "Oyo, Or, Ol, On, Oo": [{
        "Oyo East": "oye"
    }, {
        "Oyo West": "oyw"
    }, {
        "Ori Ire": "ori"
    }, {
        "Oluyole": "olu"
    }, {
        "Ona Ora": "ono"
    }, {
        "Oorelope": "oor"
    }, {
        "Olorunsogo": "olo"
    }],
    "S": ["Saki East", "Saki West", "Surulere"]
}


class Registration(Menu, Request):
    """
    New User Registration
    """

    def __init__(self, session_id, session_data, user_option, user,
                 phone_number, level, base_url):
        Menu.__init__(self, session_id, session_data, user_option,
                      user, phone_number, level)
        Request.__init__(self, base_url)

    def end_session(self):
        return self.ussd_end("Goodbye")

    def get_fullname(self):
        text = """\
      Input Fullname
      (Surname Firstname Middlename)
  """
        self.session_data['level'] = 2
        return self.ussd_proceed(text)

    def get_gender(self):
        text = """\
      Select Gender
      1. Male
      2. Female
  """
        name = self.user_option.split('+')
        if len(name) < 2:
            raise Exception('Provide your fullname')
        self.user.update({
            "lastName": name[0],
            "firstName": name[1],
            "middleName": name[2] if len(name) > 2 else None
        })
        self.session_data['level'] = 3
        return self.ussd_proceed(text)

    def get_dob(self):
        text = """
    Input Date of Birth
    (DD-MM-YYYY)
  """
        gender = {1: 'Male', 2: ' Female'}
        self.user['gender'] = gender[int(self.user_option)]
        self.session_data['level'] = 4
        return self.ussd_proceed(text)

    def get_lga(self):
        dob = re.split('[\*\./-]', self.user_option)
        if len(dob) != 3:
            raise Exception('Invalid date input format')
        self.user['dob'] = datetime.date(int(dob[2]), int(dob[1]), int(dob[0]))
        text = 'Your LGA starts with?\n'
        n = 0
        data = {}
        for x, y in lga.items():
            n += 1
            text += f"{n}. {x}\n"
            data.update({str(n): y})
        self.session_data['level'] = 5
        self.session_data["lga_dict"] = data
        return self.ussd_proceed(text)

    def display_lga_options(self):
        text = 'Select your Local Govt. Area\n'
        data = {}
        lga_dict = self.session_data["lga_dict"]
        for x, y in enumerate(lga_dict[self.user_option]):
            text += f"{x+1}. {list(y.keys())[0]}\n"
            data.update({str(x + 1): y})
        self.session_data['level'] = 6
        self.session_data["lga_dict"] = data
        return self.ussd_proceed(text)

    def get_town(self):
        text = "Slect a district closest to you\n"
        data = {}
        lga_dict = self.session_data["lga_dict"]
        self.user['lga'] = list(lga_dict[self.user_option].keys())[0]
        lga_dict = self.session_data["lga_dict"]
        threeChar = list(lga_dict[self.user_option].values())[0]
        lga = self.make_request("get", f"/lga?threeChar={threeChar}")
        for x, y in enumerate(lga['data'][0]['districts']):
            text += f"{x+1}. {y}\n"
            data.update({str(x + 1): y})
        self.session_data['level'] = 7
        self.session_data['town_dict'] = data
        return self.ussd_proceed(text)

    def get_hospital(self):
        text = "Select your preferred hospital\n"
        data = {}
        town_dict = self.session_data["town_dict"]
        self.user['town'] = town_dict[self.user_option]

        hospitals = self.make_request("get", "/hospital")
        for x, y in enumerate(hospitals['data']):
            text += f"{x+1}. {y['name']}\n"
            data.update({str(x + 1): y['_id']})
        self.session_data['level'] = 8
        self.session_data['hospital_dict'] = data
        return self.ussd_proceed(text)

    def get_pharmacy(self):
        text = "Select your preferred pharmacy\n"
        data = {}
        hospital_dict = self.session_data["hospital_dict"]
        self.user['pref_hospital'] = hospital_dict[self.user_option]
        pharmacies = self.make_request("get", "/pharmacy")
        for x, y in enumerate(pharmacies['data']):
            text += f"{x+1}. {y['name']}\n"
            data.update({str(x + 1): y['_id']})
        self.session_data['level'] = 9
        self.session_data['pharmacy_dict'] = data
        return self.ussd_proceed(text)

    def get_laboratory(self):
        text = "Select your preferred laboratory\n"
        data = {}
        pharmacy_dict = self.session_data["pharmacy_dict"]
        self.user['pref_pharmacy'] = pharmacy_dict[self.user_option]
        laboratories = self.make_request("get", "/laboratory")
        for x, y in enumerate(laboratories['data']):
            text += f"{x+1}. {y['name']}\n"
            data.update({str(x + 1): y['_id']})
        self.session_data['level'] = 10
        self.session_data['laboratory_dict'] = data
        return self.ussd_proceed(text)

    def create_citizen(self):
        laboratory_dict = self.session_data["pharmacy_dict"]
        self.user['pref_laboratory'] = laboratory_dict[self.user_option]
        self.user['phone'] = self.phone_number
        citizen = self.make_request("post", "/citizen", self.user)
        return self.ussd_end("""
                                Registration Successful
                                Thank You!
                             """)

    def execute(self):
        try:
            if (self.level == 1) and (self.user_option == '2'):
                return self.end_session()
            elif (self.level == 1) and (self.user_option == '1'):
                return self.get_fullname()
            else:
                menu = {
                    2: self.get_gender,
                    3: self.get_dob,
                    4: self.get_lga,
                    5: self.display_lga_options,
                    6: self.get_town,
                    7: self.get_hospital,
                    8: self.get_pharmacy,
                    9: self.get_laboratory,
                    10: self.create_citizen,
                }
                return menu.get(self.level)()
        except Exception as e:
            return self.ussd_end(str(e))
