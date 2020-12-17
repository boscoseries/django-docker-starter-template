import re
import datetime
from django.core.cache import cache
from django.shortcuts import render, reverse, redirect
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .serializers import UserSerializer
from urllib.parse import unquote
from django.http import HttpResponse, HttpResponseRedirect
from .user_responses import response_text, lga, town, hospitals, laboratories, pharmacies
from .utils import create_response
from .models import User
import user.user_responses as r


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
            session_data['level'] = "0"
            cache.set(phone_number, session_data)
        else:
            session_data = session

        option = text.split('*')[-1]
        response = ''

        user = r.user_exists(phone_number)

        if not user['exists']:
            try:
                """
                New User Registration

                """
                print(session_data, 'top _level', option, text)
                if session_data['level'] == "0":
                    session_data['level'] = "1"
                    cache.set(phone_number, session_data)
                    response = r.introduction()

                elif (session_data['level']) == "1" and (text == '1'):
                    session_data['level'] = "2"
                    cache.set(phone_number, session_data)
                    response = r.get_fullname()

                elif (session_data['level']) == "1" and (text == '2'):
                    cache.delete(phone_number)
                    response = quit()

                elif (session_data['level']
                      == "2") and (len(option.split('+')) >= 2):
                    name = option.split('+')
                    session_data['lastName'] = name[0]
                    session_data['firstName'] = name[1]
                    session_data['middleName'] = name[2] if len(
                        name) > 2 else None
                    session_data['level'] = "3"
                    cache.set(phone_number, session_data)
                    response = r.get_gender()

                elif session_data['level'] == "3" and (text.split('*')[-1]
                                                       in ['1', '2']):
                    if option == '1':
                        session_data['gender'] = "MALE"
                    elif option == '2':
                        session_data['gender'] = "FEMALE"
                    session_data['level'] = "4"
                    cache.set(phone_number, session_data)
                    response = r.get_dob()

                elif session_data['level'] == "4":
                    dob = re.split('[\*\./-]', option)
                    if len(dob) != 3:
                        raise Exception()

                    session_data['dob'] = datetime.date(
                        int(dob[2]), int(dob[1]), int(dob[0]))
                    session_data['level'] = "5"
                    cache.set(phone_number, session_data)
                    response = r.get_lga()

                elif (session_data['level'] == "5") & (option == '99') & (
                        session_data.get('group') is None):
                    session_data['level'] = "5"
                    session_data['group'] = 'lga'
                    cache.set(phone_number, session_data)
                    response = r.get_lga_page_two()

                elif (session_data['level'] == "5") & (option == '88') & (
                        session_data.get('group') == 'lga'):
                    session_data['level'] = "5"
                    session_data['group'] = None
                    cache.set(phone_number, session_data)
                    response = r.get_lga_page_one()

                elif (session_data['level'] == "5") & (option in [
                        '9', '10'
                ]) & (session_data.get('group') == 'lga'):
                    session_data['level'] = "5"
                    session_data['group'] = None
                    cache.set(phone_number, session_data)
                    if option == '9':
                        response = r.get_lga_group_one()
                    else:
                        response = r.get_lga_group_two()

                elif (session_data['level'] == "5") & (option == '88') & (
                        session_data.get('group') is None):
                    session_data['level'] = "5"
                    session_data['group'] = 'lga'
                    cache.set(phone_number, session_data)
                    response = r.get_lga_page_two()

                elif (session_data['level'] == "5") & (option in [
                        '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
                        '11', '12', '13'
                ]) & (session_data.get('group') is None):
                    session_data['lga'] = lga[option]
                    session_data['level'] = "6"
                    cache.set(phone_number, session_data)
                    response = r.get_town_page_one()

                elif (session_data['level'] == "5") & (option in [
                        '9', '10'
                ]) & (session_data.get('group') == 'lga'):
                    session_data['level'] = "5"
                    cache.set(phone_number, session_data)
                    response = r.get_town_page_one()

                elif (session_data['level'] == "6") & (
                        option in ['1', '2', '3', '4', '5', '6', '7', '8']):
                    hospital_dict, response = r.get_hospitals()
                    session_data['town'] = town[option]
                    session_data['level'] = "7"
                    session_data['hospitals'] = hospital_dict
                    cache.set(phone_number, session_data)

                elif session_data['level'] == "7" and (option in [
                        '1', '2', '3', '4', '5', '6', '7', '8'
                ]):
                    pharmacy_dict, response = r.get_pharmacies()
                    session_data['pref_hospital'] = session_data['hospitals'][
                        option]
                    session_data.pop('hospitals')
                    session_data['level'] = "8"
                    session_data['pharmacies'] = pharmacy_dict
                    cache.set(phone_number, session_data)

                elif session_data['level'] == "8" and (option in [
                        '1', '2', '3', '4', '5'
                ]):
                    laboratory_dict, response = r.get_laboratories()
                    session_data['pref_pharmacy'] = session_data['pharmacies'][
                        option]
                    session_data.pop('pharmacies')
                    session_data['level'] = "9"
                    session_data['laboratories'] = laboratory_dict
                    cache.set(phone_number, session_data)

                elif session_data['level'] == "9" and (option in [
                        '1', '2', '3', '4', '5'
                ]):
                    session_data['pref_laboratory'] = session_data[
                        'laboratories'][option]
                    session_data['phone'] = phone_number
                    session_data.pop('laboratories')
                    session_data.pop('level')
                    session_data.pop('group') if session_data.get(
                        'group') is not None else None
                    new_user = r.create_user(session_data)
                    if new_user['success']:
                        response = r.success()
                        cache.delete(phone_number)
                    else:
                        raise Exception()
                else:
                    raise Exception('something went wrong')
                return HttpResponse(response, content_type="text/plain")
            except Exception as e:
                cache.delete(phone_number)
                response = create_response(response_text['error'], str(e))
                return HttpResponse(response, content_type="text/plain")

        if user['exists']:
            try:
                """
                    Returning User

                """
                print(session_data, 'top _level', option, text)
                if (session_data['level'] == '0'):
                    response = r.select_service(user['obj']['lastName'])
                    session_data['level'] = "1"
                    cache.set(phone_number, session_data)

                elif (session_data['level'] == '1') and option and (option in [
                        '1', '2', '3', '4', '5', '6'
                ]) and (session_data.get('request_type') is None):
                    session_data['level'] = "2"
                    if option is None:
                        raise Exception('something went wrong 1')
                    if option == '1':
                        response = r.request_doctor_engagement()
                        cache.delete(phone_number)
                    if option == '2':
                        session_data['request_type'] = "consultation"
                        cache.set(phone_number, session_data)
                        response = r.book_physical_consultation()
                    if option == '3':
                        session_data['request_type'] = "prescription"
                        cache.set(phone_number, session_data)
                        response = r.check_prescription()
                    if option == '4':
                        session_data['request_type'] = "tests"
                        cache.set(phone_number, session_data)
                        response = r.run_tests()
                    if option == '5':
                        session_data['request_type'] = "hospital"
                        cache.set(phone_number, session_data)
                        response = r.engage_hospitals()
                    if option == '6':
                        response = r.book_health_taxi()
                        cache.delete(phone_number)

                elif (session_data['level']
                      == '2') and (session_data['request_type']
                                   == 'consultation') and option and (
                                       option in ['1', '2', '3']):
                    if option == '1':
                        response = r.request_doctor_engagement()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.request_doctor_engagement()
                        cache.delete(phone_number)
                    if option == '3':
                        response = r.request_doctor_engagement()
                        cache.delete(phone_number)

                elif (session_data['level'] == '2') and (
                        session_data['request_type']
                        == 'prescription') and option and (option in ['1']):
                    response = r.prescription_unavailable()
                    session_data['level'] = "2.3.1"
                    cache.set(phone_number, session_data)

                elif (session_data['level']
                      == '2.3.1') and (session_data['request_type']
                                       == 'prescription') and option and (
                                           option in ['1', '2']):
                    if option == '1':
                        response = r.prescription_will_get_back()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.session_end()
                        cache.delete(phone_number)

                elif (session_data['level'] == '2' and
                      (session_data['request_type']
                       == 'tests')) and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.test_type_unavailable()
                        session_data['level'] = "2.4.2"
                        cache.set(phone_number, session_data)
                    if option == '2':
                        response = r.tests_type()
                        session_data['level'] = "2.4.3"
                        cache.set(phone_number, session_data)

                elif (session_data['level']
                      == '2.4.2') and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.laboratory_will_get_back()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.session_end()
                        cache.delete(phone_number)

                elif (session_data['level']
                      == '2.4.3') and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.test_type_unavailable()
                        session_data['level'] = "2.4.4"
                        cache.set(phone_number, session_data)
                    if option == '2':
                        response = r.test_type_unavailable()
                        session_data['level'] = "2.4.5"
                        cache.set(phone_number, session_data)

                elif (session_data['level']
                      == '2.4.4') and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.laboratory_will_get_back()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.session_end()
                        cache.delete(phone_number)

                elif (session_data['level']
                      == '2.4.5') and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.laboratory_will_get_back()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.session_end()
                        cache.delete(phone_number)

                elif (session_data['level'] == '2' and
                      (session_data['request_type']
                       == 'hospital')) and option and (option
                                                       in ['1', '2', '3']):
                    if option == '1':
                        response = r.hospital_unavailable()
                    if option == '2':
                        response = r.hospital_unavailable()
                    if option == '3':
                        response = r.hospital_unavailable()

                    session_data['level'] = "2.5.1"
                    cache.set(phone_number, session_data)

                elif (session_data['level']
                      == '2.5.1') and option and (option in ['1', '2']):
                    if option == '1':
                        response = r.hospital_will_get_back()
                        cache.delete(phone_number)
                    if option == '2':
                        response = r.session_end()
                        cache.delete(phone_number)
                else:
                    raise Exception('something went wrong 7')

                return HttpResponse(response, content_type="text/plain")
            except Exception as e:
                cache.delete(phone_number)
                response = create_response(response_text['error'], str(e))
                return HttpResponse(response, content_type="text/plain")
