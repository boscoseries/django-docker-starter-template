import requests
from django.conf import settings


def make_request(method, path, data=None):
    """
    method = Request method can be "get", "post", "put", "patch" or "delete"\n
    path = A string representing the full path to the requested page. E.g. "/music/bands/?name=amaka"\n
    data = Optional Request data
    """
    try:
        method = method.lower()
        if method == "get":
            result = requests.request(method,
                                      '{}'.format(settings.BASE_URL),
                                      data=None)
            return result.json()
    except Exception as e:
        return str(e)
