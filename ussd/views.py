from django.shortcuts import render
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response


# Create your views here.

response = ''

@api_view(['GET', 'POST'])
def get_ussd(request):

  # global response
  # print(request)
  # session_id = request.values.get("sessionId", None)
  # service_code = request.values.get("serviceCode", None)
  # phone_number = request.values.get("phoneNumber", None)
  # text = request.values.get("text", "default")
  
  session_id = request.query_params.get("sessionId", None)
  phone_number = request.query_params.get("phoneNumber", None)
  text = request.query_params.get('text', 'default')
  print(text)
  response = ''
  if text == '':
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
  return Response(response, status=status.HTTP_200_OK)

