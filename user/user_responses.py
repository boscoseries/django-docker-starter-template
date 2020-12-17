import requests
from django.conf import settings
from .utils import create_response
from django.http import HttpResponse

lga = {
    "1": "Akinyele",
    "2": "Iseyin",
    "3": "Oluyole",
    "4": "Ibadan North",
    "5": "Ibadan North East",
    "6": "Ibadan North West",
    "7": "Ibadan South East",
    "8": "Ibadan South West",
    "9": "Lagelu",
    "10": "Egbeda",
    "11": "Ona Ara",
    "12": "Iwajowa",
    "13": "Kajola",
    "14": "Atisbo",
    "15": "Itesiwaju",
    "16": "Saki East",
    "17": "Saki West",
    "18": "Ibarapa North",
    "19": "Ibarapa East",
    "20": "Ibarapa Central",
    "21": "Ido",
    "22": "Ori Ire",
    "23": "Oyo West",
    "24": "Oyo East",
    "25": "Afijio",
    "26": "Oluyole",
    "27": "Ogbomosho North",
    "28": "Ogbomosho South",
    "29": "Surulere",
    "30": "Ogo Oluwa",
    "31": "Irepo",
    "32": "Orelope",
    "33": "Olorunsogo"
}

town = {
    "1": "town 1",
    "2": "town 2",
    "3": "town 3",
    "4": "town 4",
    "5": "town 5",
    "6": "town 6",
    "7": "town 7",
    "8": "town 8",
    "9": "town 9",
    "10": "town 10",
    "11": "town 11",
    "12": "town 12",
    "13": "town 13",
    "14": "town 14",
    "15": "town 15",
    "16": "town 16",
    "17": "town 17",
    "18": "town 18",
    "19": "town 19",
    "20": "town 20",
}

response_text = {
    "4": "CON Select Local Govt. Area",
    "4.1": "1. {}".format(lga['1']),
    "4.2": "2. {}".format(lga['2']),
    "4.3": "3. {}".format(lga['3']),
    "4.4": "4. {}".format(lga['4']),
    "4.5": "5. {}".format(lga['5']),
    "4.6": "6. {}".format(lga['6']),
    "4.7": "7. {}".format(lga['7']),
    "4.8": "8. {}".format(lga['8']),
    "4.9": "CON 9. Lagelu, Egbeda, Ona Ara",
    "4.10": "10. Iwajowa, Kajola",
    "5": "CON Select Town / Community",
    "5.1": "1. {}".format(town['1']),
    "5.2": "2. {}".format(town['2']),
    "5.3": "3. {}".format(town['3']),
    "5.4": "4. {}".format(town['4']),
    "5.5": "5. {}".format(town['5']),
    "99": "99. Next",
    "88": "88. Back",
    "error": "END Error Ocurred",
}


def create_user(data):
    try:
        user = requests.post('{}/citizen'.format(settings.BASE_URL), data=data)
        if user.status_code == 201:
            return {'success': True}
    except Exception as e:
        return {'success': False, 'message': str(e)}


def introduction():
    return """
    CON Welcome to Oyo State Tele-medicine Service
    1. Register
    2. Exit
"""


def quit():
    return "END Goodbye"


def success():
    return """
    END Registration Successful
    Thank You!
"""


def get_fullname():
    return """
    CON Input Fullname
    (Surname Firstname Middlename)
"""


def get_gender():
    return """
    CON Select Gender
    1. Male
    2. Female
"""


def get_dob():
    return """
    CON Input Date of Birth"
    (DD-MM-YYYY)
"""


def get_lga():
    return create_response(
        response_text['4'],
        response_text['4.1'],
        response_text['4.2'],
        response_text['4.3'],
        response_text['4.4'],
        response_text['4.5'],
        response_text['4.6'],
        response_text['4.7'],
        response_text['4.8'],
        response_text['99'],
    )


def get_lga_page_one():
    return create_response(
        response_text['4'],
        response_text['4.1'],
        response_text['4.2'],
        response_text['4.3'],
        response_text['4.4'],
        response_text['4.5'],
        response_text['4.6'],
        response_text['4.7'],
        response_text['4.8'],
        response_text['99'],
    )


def get_lga_page_two():
    return create_response(
        response_text['4.9'],
        response_text['4.10'],
        response_text['88'],
    )


def get_lga_group_one():
    return """
    CON 9. Lagelu
    10. Egbeda
    11. Ona Ara
    88. Back
"""


def get_lga_group_two():
    return """
    CON 12. Iwajowa
    13. Kajola
    88. Back
"""


def get_town_page_one():
    return create_response(response_text['5'], response_text['5.1'],
                           response_text['5.2'], response_text['5.3'],
                           response_text['5.4'], response_text['5.5'])


def get_hospitals():
    try:
        response = 'CON Select Preferred Hospital\n'
        hospital_dict = {}
        hospitals = requests.get('{}/hospital'.format(settings.BASE_URL))
        for i, j in enumerate(hospitals.json()['data']):
            hospital_dict[str(i + 1)] = j['_id']
            response = response + f"{i+1}. {j['name']}\n"
        return [hospital_dict, response]
    except Exception as e:
        return str(e)


def get_pharmacies():
    try:
        response = 'CON Select Preferred Pharmacy\n'
        pharmacy_dict = {}
        pharmacies = requests.get('{}/pharmacy'.format(settings.BASE_URL))
        for i, j in enumerate(pharmacies.json()['data']):
            pharmacy_dict[str(i + 1)] = j['_id']
            response = response + f"{i+1}. {j['name']}\n"
        return [pharmacy_dict, response]
    except Exception as e:
        return str(e)


def get_laboratories():
    try:
        response = 'CON Select Preferred Laboratory\n'
        laboratory_dict = {}
        laboratories = requests.get('{}/laboratory'.format(settings.BASE_URL))
        for i, j in enumerate(laboratories.json()['data']):
            laboratory_dict[str(i + 1)] = j['_id']
            response = response + f"{i+1}. {j['name']}\n"
        return [laboratory_dict, response]
    except Exception as e:
        return str(e)


def select_service(firstname):
    return """
    CON Welcome {}, what would you like to do today?
    1. Request Doctor Engagement
    2. Book Physical Consultation
    3. Check Prescription
    4. Run Tests
    5. Engage Hospital
    6. Book Health Taxi
""".format(firstname)


def doctor_will_get_back():
    return """
    END Received.
    Doctor will get back to you.
"""


def request_doctor_engagement():
    return """
    END Received.
    Doctor will get back to you.
"""


def book_physical_consultation():
    return """
    CON Doctor's area of specialization.
    1. Surgery
    2. Dentistry
    3 Optometry
"""


def check_prescription():
    return """
    CON 1. Purchase Prescription
"""


def prescription_unavailable():
    return """
    CON Not available in preferred pharmacy, will you like to proceed to another pharmacy?
    1. Yes
    2. No
"""


def prescription_will_get_back():
    return """
    END Received.
    Pharmacy will get back to you.
"""


def session_end():
    return """
    END Received.
    Session ended!
"""


def run_tests():
    return """
    CON Select Service
    1. Check recommendadtions
    2. Select test type
"""


def tests_type():
    return """
    CON 1. option 1
    2. option 2
"""


def test_type_unavailable():
    return """
    CON Not available in preferred laboratory, will you like to proceed to another laboratory?
    1. Yes
    2. No
"""


def laboratory_will_get_back():
    return """
    END Received.
    Laboratory will get back to you.
"""


def engage_hospitals():
    return """
    CON Select Service.
    1. Doctor
    2. Pharmacy
    3. Laboratory
"""


def hospital_unavailable():
    return """
    CON Not available in preferred hospital, will you like to proceed to another hospital?
    1. Yes
    2. No
"""


def hospital_will_get_back():
    return """
    END Received.
    Hospital will get back to you.
"""


def book_health_taxi():
    return """
    END Received.
    Health Taxi will get back to you.
"""