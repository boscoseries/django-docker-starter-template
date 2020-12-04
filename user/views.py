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
        text = request_dict.get('text', 'res')

        session = cache.get(phone_number)
        session_data = {}

        if session is None:
            session_data = {'phone_number': phone_number, 'level': '0'}
            cache.set(phone_number, session_data)
        else:
            session_data = session

        try:
            option = text.split('*')[-1]
            response = ''
            user = get_user_model().objects.filter(
                phone_number=phone_number).first()

            if session_data['level'] == "0":
                if user is None:
                    response = create_response(response_text['0'],
                                               response_text['0*1'],
                                               response_text['0*2'])
                    session_data['level'] = "1"
                    cache.set(phone_number, session_data)
            elif session_data['level'] == "1":
                if text not in ['1', '2']:
                    raise Exception()

                response = create_response(response_text['1'],
                                           response_text['1-details'])
                session_data['level'] = "2"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "2":
                if len(text.split('*')) != 2 or (len(option.split('+')) < 2):
                    raise Exception('Input all names')

                session_data['fullname'] = text.split('*')[-1].replace(
                    '+', ' ')
                response = create_response(response_text['1*s'],
                                           response_text['1*s*1'],
                                           response_text['1*s*2'])
                session_data['level'] = "3"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "3":
                if len(text.split('*')) != 3 or (text.split('*')[-1]
                                                 not in ['1', '2']):
                    raise Exception('Invalid Input')

                if option == '1':
                    session_data['gender'] = "MALE"
                elif option == '2':
                    session_data['gender'] = "FEMALE"
                response = create_response(response_text['1*s*d*s'],
                                           response_text['1*s*d*s-ddmmyy'])
                session_data['level'] = "4"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "4":
                date = text.split('*')[-1]
                dob = re.split('[\*\./-]', date)
                if len(text.split('*')) != 4 or (len(dob) != 3):
                    raise Exception()

                session_data['date_of_birth'] = datetime.date(
                    int(dob[2]), int(dob[1]), int(dob[0]))
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
            elif session_data['level'] == "5":
                if len(text.split('*')) != 5 or (option not in [
                        '1', '2', '3', '4', '5', '6', '99'
                ]):
                    raise Exception()

                session_data['lga'] = lga[option]
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
            elif session_data['level'] == "6":
                if len(text.split('*')) != 6 or (option not in [
                        '1', '2', '3', '4', '5', '6', '99'
                ]):
                    raise Exception()

                session_data['town'] = town[option]
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
            elif session_data['level'] == "7":
                if len(text.split('*')) != 7 or (option not in [
                        '1', '2', '3', '4', '5', '6', '99'
                ]):
                    raise Exception()

                session_data['preferred_hospital'] = hospitals[option]
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
            elif session_data['level'] == "8":
                if len(text.split('*')) != 8 or (option not in [
                        '1', '2', '3', '4', '5', '6', '99'
                ]):
                    raise Exception()
                session_data['preferred_pharmacy'] = pharmacies[option]
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
            elif session_data['level'] == "9":
                if len(text.split('*')) != 9 or (option not in [
                        '1', '2', '3', '4', '5', '6', '99'
                ]):
                    raise Exception()
                session_data['preferred_laboratory'] = laboratories[option]
                session_data['phone_number'] = phone_number
                session_data.pop('level')

                new_user = User(**session_data)
                new_user.set_password('password')
                new_user.save()
                response = create_response(response_text['2'],
                                           response_text['2*1'])
                cache.delete(phone_number)
            return HttpResponse(response, content_type="text/plain")
        except Exception as e:
            cache.delete(phone_number)
            response = create_response(response_text['error'], str(e))
            return HttpResponse(response, content_type="text/plain")
