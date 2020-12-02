from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model
from .serializers import UserSerializer
from urllib.parse import unquote
from django.http import HttpResponse



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

      response = None
      if text == '' or text is None:
        response  = "CON What would you want to check \n"
        response += "1. My Account \n"
        response += "2. My phone number"
      elif text == '1':
        response = "CON Choose account information you want to view \n"
        response += "1. Account number \n"
        response += "2. Account balance"
      elif text == '1*1':
        accountNumber  = "ACC1001"
        response = "END Your account number is " + accountNumber
      elif text == '1*2':
        balance  = "KES 10,000"
        response = "END Your balance is " + balance
      elif text == '2':
        response = "END This is your phone number " + "phone_number"
      return HttpResponse(response, content_type="text/plain")

