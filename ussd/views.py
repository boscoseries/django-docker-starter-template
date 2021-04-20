import datetime
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import api_view
from .utils import decode_request
from django.http import HttpResponse
from .register import Registration
from .decorators import thread
from ussd.engagement import (Doctor, Consult, Prescribe, Hospital, LabTests)
from ussd.requests import Request
from sentry_sdk import capture_exception
req = Request(base_url=None)


@api_view(['POST'])
@thread
def ussd_callback(request, *args, **kwargs):
    try:
        phone, session_id, text = decode_request(request)
        phone = phone.replace('+234', '0')
        citizen = req.make_request('post',
                                   '/citizen',
                                   data={
                                       "action": "check-unique",
                                       "phone": phone
                                   })

        if citizen.get('unique'):
            session_data = cache.get_or_set(session_id,
                                            {"user": {
                                                "phone": phone
                                            }})
            register = Registration(session_id=session_id,
                                    session_data=session_data,
                                    user_option=text.split('*')[-1],
                                    base_url=None,
                                    level=int(
                                        cache.get(session_id).get('level', 0)))

            if not session_data.get("level"):
                session_data['level'] = 1
                return register.home()

            if session_data.get("level") >= 1:
                return register.execute()

            raise Exception('Something went wrong!')
        else:
            session_data = cache.get_or_set(session_id, {
                "user": citizen['data'][0],
                "menu": "home"
            })

            doctor = Doctor(session_id=session_id,
                            session_data=session_data,
                            user_option=text.split('*')[-1],
                            base_url=None,
                            level=int(cache.get(session_id).get('level', 0)))
            if session_data.get('menu') == 'home' or (text.split('*')[-1]
                                                      == '99'):
                session_data.update({"level": 0, "base": True, "menu": None})
                return doctor.start()

            if (session_data.get('menu')
                    == 'engage_doctor') or (session_data['base'] and
                                            (text.split('*')[-1] == "1")):
                return doctor.execute()

            if (session_data.get('menu')
                    == 'prescription') or (session_data['base'] and
                                           (text.split('*')[-1] == "2")):
                prescription = Prescribe(
                    session_id=session_id,
                    session_data=session_data,
                    user_option=text.split('*')[-1],
                    base_url=None,
                    level=int(cache.get(session_id).get('level', 0)))
                return prescription.execute()

            if (session_data.get('menu')
                    == 'lab_tests') or (session_data['base'] and
                                        (text.split('*')[-1] == "3")):
                lab_tests = LabTests(session_id=session_id,
                                     session_data=session_data,
                                     user_option=text.split('*')[-1],
                                     base_url=None,
                                     level=int(
                                         cache.get(session_id).get('level',
                                                                   0)))
                return lab_tests.execute()

            if (session_data.get('menu')
                    == 'engage_hospital') or (session_data['base'] and
                                              (text.split('*')[-1] == "4")):
                hospital = Hospital(session_id=session_id,
                                    session_data=session_data,
                                    user_option=text.split('*')[-1],
                                    base_url=None,
                                    level=int(
                                        cache.get(session_id).get('level', 0)))
                return hospital.execute()

            if (session_data.get('menu')
                    == 'health_taxi') or (session_data['base'] and
                                          (text.split('*')[-1] == "5")):
                return doctor.start()

            raise Exception('Something went wrong!')
    except Exception as e:
        capture_exception(e)
        return HttpResponse("Something went wrong!", content_type="text/plain")