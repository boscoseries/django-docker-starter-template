import re
import datetime
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
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

        try:
            response = ''

            user = get_user_model().objects.filter(
                phone_number=phone_number).first()
            new_user = User()

            if text == '' or text == None:
                if user is None:
                    response = create_response(response_text['0'],
                                               response_text['0*1'],
                                               response_text['0*2'])
            elif text == '1' and user is None:
                response = create_response(response_text['1'],
                                           response_text['1-details'])
            elif re.match(r"^1\*[\w+\w+]+$", text) and user is None:
                text_data = re.match(r"^1\*[\w+\w+]+$", text).group()
                new_user.fullname = text_data.split('*')[-1].replace('+', ' ')
                response = create_response(response_text['1*s'],
                                           response_text['1*s*1'],
                                           response_text['1*s*2'])
            elif re.match(r"^1\*[\w+\w+]+\*[12]$", text) and user is None:
                text_data = re.match(r"^1\*[\w+\+\w+]+\*[12]$", text).group()
                mf = text_data.split('*')[-1]
                if mf == '1':
                    new_user.gender = "MALE"
                elif mf == '2':
                    new_user.gender = "FEMALE"
                response = create_response(response_text['1*s*d*s'],
                                           response_text['1*s*d*s-ddmmyy'])
            elif re.match(r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}$",
                          text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}$",
                    text).group()
                dob = re.split('[\*\./-]', text)
                new_user.date_of_birth = datetime.date(int(dob[-1]),
                                                       int(dob[-2]),
                                                       int(dob[-3]))
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
            elif re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]$",
                    text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]$",
                    text).group()
                index = text_data.split('*')[-1]
                new_user.lga = lga[index]
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
            elif re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]$",
                    text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]$",
                    text).group()
                index = text_data.split('*')[-1]
                new_user.town = town[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d'],
                    response_text['1*s*d*s*s*d*d-hos*1'],
                    response_text['1*s*d*s*s*d*d-hos*2'],
                    response_text['1*s*d*s*s*d*d-hos*3'],
                    response_text['1*s*d*s*s*d*d-hos*4'],
                    response_text['1*s*d*s*s*d*d-hos*5'],
                )
            elif re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]$",
                    text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                new_user.preferred_hospital = hospitals[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d*d'],
                    response_text['1*s*d*s*s*d*d*d-pha*1'],
                    response_text['1*s*d*s*s*d*d*d-pha*2'],
                    response_text['1*s*d*s*s*d*d*d-pha*3'],
                    response_text['1*s*d*s*s*d*d*d-pha*4'],
                    response_text['1*s*d*s*s*d*d*d-pha*5'],
                )
            elif re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]$",
                    text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                new_user.preferred_pharmacy = pharmacies[index]
                response = create_response(
                    response_text['1*s*d*s*s*d*d*d*d'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*1'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*2'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*3'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*4'],
                    response_text['1*s*d*s*s*d*d*d*d-lab*5'],
                )
            elif re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]\*[12345]$",
                    text) and user is None:
                text_data = re.match(
                    r"^1\*[\w+\w+]+\*[12]\*\d{2}[-/.]\d{2}[-/.]\d{4}\*[12345678]\*[12345678]\*[12345]\*[12345]\*[12345]$",
                    text).group()
                index = text_data.split('*')[-1]
                new_user.preferred_laboratory = laboratories[index]
                new_user.phone_number = phone_number
                new_user.set_password('password')
                new_user.save()
                response = create_response(response_text['2'],
                                           response_text['2*1'])
            return HttpResponse(response, content_type="text/plain")
        except Exception as e:
            response = create_response(response_text['error'], str(e))
            return HttpResponse(response, content_type="text/plain")
