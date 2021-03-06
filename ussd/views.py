import datetime
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model

from .serializers import USSDSerializer
from urllib.parse import unquote
from django.http import HttpResponse
from .register import Registration
from ussd.engagement import (Doctor, Consult, Prescribe, Hospital, LabTests)
from ussd.requests import Request
from sentry_sdk import capture_exception

req = Request(base_url=None)


class USSDViewsets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = USSDSerializer
    http_method_names = ['get', 'post']

    def create(self, request, *args, **kwargs):

        url_params = unquote(request.body.decode("utf"))
        request_dict = dict((x.strip(), y.strip())
                            for x, y in (element.split('=')
                                         for element in url_params.split('&')))
        session_id = request_dict.get("sessionId", None)
        service_code = request_dict.get("serviceCode", None)
        phone_number = request_dict.get("phoneNumber", None)
        network_code = request_dict.get('networkCode', None)
        text = request_dict.get('text', None)
        phone_number = phone_number.replace('+234', '0')
        session = cache.get(session_id)
        session_data = {}

        try:
            citizen = req.make_request('post', '/citizen', data={"action": "check-unique", "phone": phone_number })
            if session is None:
                session_data['level'] = 0
                session_data['engagement'] = True if citizen.get('unique') == False else None
                session_data['menu'] = 'home' if citizen.get('unique') == False else None
                cache.set(session_id, session_data)
                user = cache.set(f"user{phone_number}", {"phone": phone_number})
            else:
                session_data = session

            user_option = text.split('*')[-1]
            level = int(session_data.get('level'))

            data = {
                "session_id": session_id,
                "session_data": session_data,
                "user_option": user_option,
                "user": citizen['data'][0] if citizen.get('unique') == False else cache.get(f"user{phone_number}"),
                "phone_number": phone_number,
                "level": level,
                "base_url": None
            }

            if not session_data['engagement']:
                register = Registration(**data)
                if level == 0:
                    session_data['level'] = 1
                    return register.home()

                if level >= 1:
                    return register.execute()
                raise Exception('Something went wrong!')

            if session_data['engagement']:
                doctor = Doctor(**data)
                if session_data.get('menu') == 'home' or (user_option == '99'):
                    session_data.update({
                        "level": 0,
                        "base": True,
                        "menu": None
                    })
                    return doctor.start()

                if (session_data.get('menu')
                        == 'engage_doctor') or (session_data['base'] and
                                                (user_option == "1")):
                    return doctor.execute()

                if (session_data.get('menu')
                        == 'prescription') or (session_data['base'] and
                                               (user_option == "2")):
                    prescription = Prescribe(**data)
                    return prescription.execute()

                if (session_data.get('menu')
                        == 'lab_tests') or (session_data['base'] and
                                            (user_option == "3")):
                    lab_tests = LabTests(**data)
                    return lab_tests.execute()

                if (session_data.get('menu')
                        == 'engage_hospital') or (session_data['base'] and
                                                  (user_option == "4")):
                    hospital = Hospital(**data)
                    return hospital.execute()

                if (session_data.get('menu')
                        == 'health_taxi') or (session_data['base'] and
                                              (user_option == "5")):
                    return doctor.start()

                raise Exception('Something went wrong!')

        except Exception as e:
            cache.delete(session_id)
            capture_exception(e)
            return HttpResponse(str(e), content_type="text/plain")