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
            session_data = {'phone_number': phone_number, 'level': '0'}
            cache.set(phone_number, session_data)
        else:
            session_data = session

        print(session_data)
        print(text)
        try:
            option = text.split('*')[-1]
            response = ''
            user = get_user_model().objects.filter(
                phone_number=phone_number).first()

            if session_data['level'] == "0":
                if user is None:
                    response = create_response(response_text['0'],
                                               response_text['0.1'],
                                               response_text['0.2'])
                    session_data['level'] = "1"
                    cache.set(phone_number, session_data)
            elif session_data['level'] == "1":
                if text not in ['1', '2']:
                    raise Exception()

                response = create_response(response_text['1'],
                                           response_text['1.1'])
                session_data['level'] = "2"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "2":
                if len(text.split('*')) != 2 or (len(option.split('+')) < 2):
                    raise Exception('Input all names')

                session_data['fullname'] = text.split('*')[-1].replace(
                    '+', ' ')
                response = create_response(response_text['2'],
                                           response_text['2.1'],
                                           response_text['2.2'])
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
                response = create_response(response_text['3'],
                                           response_text['3.1'])
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
                session_data['level'] = "5"
                cache.set(phone_number, session_data)
            elif (session_data['level'] == "5") & (option == '99'):
                # if len(text.split('*')) != 5 or (option not in [
                #         '8', '9', '10', '11', '12', '13', '14', '15', '16',
                #         '17'
                # ]):
                #     raise Exception()

                # session_data['lga'] = lga[option]
                response = create_response(
                    response_text['4.9'],
                    response_text['4.10'],
                    response_text['4.11'],
                    response_text['4.12'],
                    response_text['4.13'],
                    response_text['4.14'],
                    response_text['4.15'],
                    response_text['4.16'],
                    response_text['4.17'],
                    response_text['88'],
                )
                session_data['level'] = "5"
                cache.set(phone_number, session_data)
            elif (session_data['level'] == "5") & (option == '88'):
                # if len(text.split('*')) != 5 or (option not in [
                #         '8', '9', '10', '11', '12', '13', '14', '15', '16',
                #         '17'
                # ]):
                #     raise Exception()

                # session_data['lga'] = lga[option]
                response = create_response(
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
                session_data['level'] = "5"
                cache.set(phone_number, session_data)
            elif (session_data['level'] == "5") & (
                    option in ['1', '2', '3', '4', '5', '6', '7', '8']):
                print('got in here level 5')
                # if len(text.split('*')) != 5 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '99'
                # ]):
                #     raise Exception()

                session_data['lga'] = lga[option]
                response = create_response(
                    response_text['5'], response_text['5.1'],
                    response_text['5.2'], response_text['5.3'],
                    response_text['5.4'], response_text['5.5'],
                    response_text['5.6'], response_text['5.7'],
                    response_text['5.8'], response_text['5.9'],
                    response_text['5.10'], response_text['5.11'])
                session_data['level'] = "7"
                cache.set(phone_number, session_data)
            elif (session_data['level'] == "5") & (option in [
                    '9', '10', '11', '12', '13', '14', '15', '16', '17'
            ]):
                # if len(text.split('*')) != 5 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '99'
                # ]):
                #     raise Exception()

                session_data['lga'] = lga[option]
                response = create_response(
                    response_text['5'], response_text['5.1'],
                    response_text['5.2'], response_text['5.3'],
                    response_text['5.4'], response_text['5.5'],
                    response_text['5.6'], response_text['5.7'],
                    response_text['5.8'], response_text['5.9'],
                    response_text['5.10'], response_text['5.11'])
                session_data['level'] = "7"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "6":
                # if len(text.split('*')) != 5 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '99'
                # ]):
                #     raise Exception()
                print('got in here level 6')

                session_data['lga'] = lga[option]
                response = create_response(
                    response_text['5'], response_text['5.1'],
                    response_text['5.2'], response_text['5.3'],
                    response_text['5.4'], response_text['5.5'],
                    response_text['5.6'], response_text['5.7'],
                    response_text['5.8'], response_text['5.9'],
                    response_text['5.10'], response_text['5.11'])
                session_data['level'] = "7"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "7":
                # if len(text.split('*')) != 6 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '8', '99'
                # ]):
                #     raise Exception()

                # if option == '99':
                #     response = create_response(
                #         response_text['6'],
                #         response_text['6.9'],
                #         response_text['6.10'],
                #     )
                #     return HttpResponse(response, content_type="text/plain")
                print('got in here level 7')

                session_data['town'] = town[option]
                response = create_response(
                    response_text['6'],
                    response_text['6.1'],
                    response_text['6.2'],
                    response_text['6.3'],
                    response_text['6.4'],
                    response_text['6.5'],
                    response_text['6.6'],
                    response_text['6.7'],
                    response_text['6.8'],
                )
                session_data['level'] = "8"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "8":
                # if len(text.split('*')) != 7 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '8', '99'
                # ]):
                #     raise Exception()
                print('got in here level 8')

                session_data['preferred_hospital'] = hospitals[option]
                response = create_response(
                    response_text['7'],
                    response_text['7.1'],
                    response_text['7.2'],
                    response_text['7.3'],
                    response_text['7.4'],
                    response_text['7.5'],
                )
                session_data['level'] = "9"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "9":
                # if len(text.split('*')) != 8 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '8', '99'
                # ]):
                # raise Exception()
                print('got in here level 9')

                session_data['preferred_pharmacy'] = pharmacies[option]
                response = create_response(
                    response_text['8'],
                    response_text['8.1'],
                    response_text['8.2'],
                    response_text['8.3'],
                    response_text['8.4'],
                    response_text['8.5'],
                )
                session_data['level'] = "10"
                cache.set(phone_number, session_data)
            elif session_data['level'] == "10":
                # if len(text.split('*')) != 9 or (option not in [
                #         '1', '2', '3', '4', '5', '6', '7', '8', '99'
                # ]):
                #     raise Exception()
                print('got in here level 10')

                session_data['preferred_laboratory'] = laboratories[option]
                session_data['phone_number'] = phone_number
                session_data.pop('level')

                new_user = User(**session_data)
                new_user.set_password('password')
                new_user.save()
                response = create_response(response_text['success'],
                                           response_text['success-1'])
                cache.delete(phone_number)
            return HttpResponse(response, content_type="text/plain")
        except Exception as e:
            cache.delete(phone_number)
            response = create_response(response_text['error'], str(e))
            return HttpResponse(response, content_type="text/plain")
