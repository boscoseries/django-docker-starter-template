import requests
from urllib.parse import unquote
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

def decode_request(req):
    url_params = unquote(req.body.decode("utf"))
    request_dict = dict(
        (x.strip(), y.strip())
        for x, y in (element.split('=')
                        for element in url_params.split('&')))
    return request_dict.get("phoneNumber", None), request_dict.get(
        "sessionId", None), request_dict.get('text', None)