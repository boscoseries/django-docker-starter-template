import requests
from django.conf import settings
from .utils import create_response
from django.http import HttpResponse

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