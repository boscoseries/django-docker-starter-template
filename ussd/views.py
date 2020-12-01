from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from django.conf import settings
from urllib.parse import unquote
from django.http import HttpResponse
from rest_framework.response import Response


# Create your views here.

response = ''

@api_view(['GET', 'POST'])
def get_ussd(request):

  url_params = unquote(request.body.decode("utf"))
  request_dict = dict((x.strip(), y.strip())
             for x, y in (element.split('=')
             for element in url_params.split('&')))

  # print(request_dict)

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