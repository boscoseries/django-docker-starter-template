import threading
import logging
import concurrent.futures as c
from django.http import HttpResponse

# https://docs.python.org/3/howto/logging.html#logging-basic-tutorial
logging.basicConfig(
    level=logging.DEBUG,
    format='%(message)s',
)


def thread(function):
    def decorator(*args, **kwargs):
        print('thread_count', threading.active_count())
        with c.ThreadPoolExecutor() as executor:
            future = executor.submit(function, *args, **kwargs)
            return_value = future.result()

        return HttpResponse(return_value, content_type="text/plain")

    return decorator
