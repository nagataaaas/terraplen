from functools import wraps
from terraplen.exception import DetectedAsBotException


def retry(func):
    @wraps(func)
    def wrapper(instance, *args, **kwargs):
        try:
            return func(instance, *args, **kwargs)
        except DetectedAsBotException:
            instance.init()
            return func(instance, *args, **kwargs)

    return wrapper
