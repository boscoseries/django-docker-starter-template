import requests
from django.conf import settings


class Request:
    def __init__(self, base_url):
        self.base_url = settings.BASE_URL

    def make_request(self, method, path, data=None):
        """
          :param method: Request method can be `GET`, `POST`, `PUT`, `PATCH` or `DELETE`\n
          :param path: A string representing the full path to the requested page. E.g. `/music/bands/?name=amaka`\n
          :param data: Optional Request data
        """
        try:
            result = requests.request(method, '{}{}'.format(self.base_url, path),
                                      data=data)
            return result.json()
        except Exception as e:
            return str(e)
