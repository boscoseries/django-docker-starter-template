import datetime
from django.core.cache import cache
from django.shortcuts import render
from rest_framework import viewsets
from django.contrib.auth import get_user_model

from .serializers import USSDSerializer
from urllib.parse import unquote
from django.http import HttpResponse
from .register import Registration
from .consult import Consultation
from ussd.requests import Request

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

        session = cache.get(session_id)
        session_data = {}

        if session is None:
            session_data['level'] = 0
            cache.set(session_id, session_data)
            cache.set("user", {"phone": phone_number})
        else:
            session_data = session

        user_option = text.split('*')[-1]
        citizen = req.make_request('post',
                                   '/citizen',
                                   data={
                                       "action": "check-unique",
                                       "phone": phone_number
                                   })

        level = int(session_data.get('level'))
        try:
            if citizen['unique']:
                register = Registration(session_id=session_id,
                                        session_data=session_data,
                                        user_option=user_option,
                                        user=cache.get('user'),
                                        phone_number=phone_number,
                                        level=level,
                                        base_url=None)
                if level == 0:
                    session_data['level'] = 1
                    return register.home()

                if level >= 1:
                    return register.execute()
                raise Exception('Something went wrong!')

            if not citizen['unique']:
                consult = Consultation(session_id=session_id,
                                       session_data=session_data,
                                       user_option=user_option,
                                       user=citizen['data'][0],
                                       phone_number=phone_number,
                                       level=level,
                                       base_url=None)
                if level == 0:
                    session_data['level'] = 1
                    return consult.start()

                if level >= 1:
                    return consult.execute()
                raise Exception('Something went wrong!')

        except Exception as e:
            return HttpResponse(str(e), content_type="text/plain")
            cache.delete(session_id)
