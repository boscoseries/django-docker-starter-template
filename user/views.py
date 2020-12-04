import re
import datetime
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .serializers import UserSerializer
from urllib.parse import unquote
from django.http import HttpResponse
from .user_responses import response_text, lga, town, hospitals, laboratories, pharmacies
from .utils import create_response
from .models import User

# Create your views here.

class UserViewsets(viewsets.ModelViewSet):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
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

        session = cache.get(phone_number)
        session_data = {}
        if session is None:
            session_data = {'phone_number': phone_number, 'level': "0"}
            cache.set(phone_number, session_data)
        else:
            session_data = session

        try:
            response = ''
            user = get_user_model().objects.filter(
                phone_number=phone_number).first()

            if text == '' or session_data['level'] == "0":
                if user is None:
                    response = create_response(response_text['0'],
                                               response_text['0*1'],
                                               response_text['0*2'])
                    session_data['level'] = "1"
                    cache.set(phone_number, session_data)
            elif (text == '1'
                  and user is None) or session_data['level'] == "1":
                response = create_response(response_text['1'],
                                           response_text['1-details'])
                session_data['level'] = "2"
                cache.set(phone_number, session_data)
            elif (re.match(r"^1\*[\w+\w+]+$", text)
                  and user is None) or session_data['level'] == "2":
                text_data = re.match(r"^1\*[\w+\w+]+$", text).group()
                session_data['fullname'] = text_data.split('*')[-1].replace(
                    '+', ' ')
                response = create_response(response_text['1*s'],
                                           response_text['1*s*1'],
                                           response_text['1*s*2'])
                session_data['level'] = "3"
                cache.set(phone_number, session_data)
            elif (re.match(r"^1\*[\w+\w+]+\*[12]$", text)
                  and user is None) or session_data['level'] == "3":
                text_data = re.match(r"^1\*[\w+\+\w+]+\*[12]$", text).group()
                mf = text_data.split('*')[-1]
                if mf == '1':
                    session_data['gender'] = "MALE"
                elif mf == '2':
                    session_data['gender'] = "FEMALE"
                response = create_response(response_text['1*s*d*s'],
                                           response_text['1*s*d*s-ddmmyy'])
                session_data['level'] = "4"
                cache.set(phone_number, session_data)
            elif (re.match(r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}$",
                           text)
                  and user is None) or session_data['level'] == "4":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}$",
                    text).group()
                dob = re.split('[\*\./-]', text)
                session_data['date_of_birth'] = datetime.date(
                    int(dob[-1]), int(dob[-2]), int(dob[-3]))
                response = create_response(
                    response_text['1*s*d*s*s'],
                    response_text['1*s*d*s*s-lga*1'],
                    response_text['1*s*d*s*s-lga*2'],
                    response_text['1*s*d*s*s-lga*3'],
                    response_text['1*s*d*s*s-lga*4'],
                    response_text['1*s*d*s*s-lga*5'],
                    response_text['1*s*d*s*s-lga*6'],
                    response_text['1*s*d*s*s-lga*7'],
                    response_text['1*s*d*s*s-lga*8'],
                    response_text['1*s*d*s*s-lga*9'],
                    response_text['1*s*d*s*s-lga*10'],
                    response_text['1*s*d*s*s-lga*11'],
                    response_text['1*s*d*s*s-lga*12'],
                    response_text['1*s*d*s*s-lga*13'],
                    response_text['1*s*d*s*s-lga*14'],
                    response_text['1*s*d*s*s-lga*15'],
                    response_text['1*s*d*s*s-lga*16'],
                    response_text['1*s*d*s*s-lga*17'],
                )
                session_data['level'] = "5"
                cache.set(phone_number, session_data)
            elif (re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]$",
                    text) and user is None) or session_data['level'] == "5":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]$",
                    text).group()
                index = text_data.split('*')[-1]
                session_data['lga'] = lga[index]
                response = create_response(response_text['1*s*d*s*s*d'],
                                           response_text['1*s*d*s*s*d-com*1'],
                                           response_text['1*s*d*s*s*d-com*2'],
                                           response_text['1*s*d*s*s*d-com*3'],
                                           response_text['1*s*d*s*s*d-com*4'],
                                           response_text['1*s*d*s*s*d-com*5'],
                                           response_text['1*s*d*s*s*d-com*6'],
                                           response_text['1*s*d*s*s*d-com*7'],
                                           response_text['1*s*d*s*s*d-com*8'],
                                           response_text['1*s*d*s*s*d-com*9'],
                                           response_text['1*s*d*s*s*d-com*10'],
                                           response_text['1*s*d*s*s*d-com*11'])
                session_data['level'] = "6"
                cache.set(phone_number, session_data)
            elif (re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]$",
                    text) and user is None) or session_data['level'] == "6":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]$",
                    text).group()
                index = text_data.split('*')[-1]
                session_data['town'] = town[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d'],
                    response_text['1*s*d*s*s*d*d-hos*1'],
                    response_text['1*s*d*s*s*d*d-hos*2'],
                    response_text['1*s*d*s*s*d*d-hos*3'],
                    response_text['1*s*d*s*s*d*d-hos*4'],
                    response_text['1*s*d*s*s*d*d-hos*5'],
                )
                session_data['level'] = "7"
                cache.set(phone_number, session_data)
            elif (re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]$",
                    text) and user is None) or session_data['level'] == "7":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                session_data['preferred_hospital'] = hospitals[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d*d'],
                    response_text['1*s*d*s*s*d*d*d-pha*1'],
                    response_text['1*s*d*s*s*d*d*d-pha*2'],
                    response_text['1*s*d*s*s*d*d*d-pha*3'],
                    response_text['1*s*d*s*s*d*d*d-pha*4'],
                    response_text['1*s*d*s*s*d*d*d-pha*5'],
                )
                session_data['level'] = "8"
                cache.set(phone_number, session_data)
            elif (re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]$",
                    text) and user is None) or session_data['level'] == "8":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                session_data['preferred_pharmacy'] = pharmacies[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d*d*d'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*1'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*2'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*3'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*4'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*5'],
                )
                session_data['level'] = "9"
                cache.set(phone_number, session_data)
            elif (re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]\*[12345]$",
                    text) and user is None) or session_data['level'] == "9":
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                session_data['preferred_laboratory'] = laboratories[index]
                session_data['phone_number'] = phone_number

                print(session_data)
                print(type(session_data))

                session_data.pop('level')
                new_user = User(**session_data)
                new_user.set_password('password')
                new_user.save()
                response = create_response(response_text['2'],
                                           response_text['2*1'])
                cache.delete(phone_number)
            return HttpResponse(response, content_type="text/plain")
        except Exception as e:
            response = create_response(response_text['error'], str(e))
            return HttpResponse(response, content_type="text/plain")
