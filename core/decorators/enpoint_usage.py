import logging
from functools import wraps
from django.conf import settings


logger = logging.getLogger("ergon_test")


class EndpointUsage:
    """
    [TASK-2] Write a decorator in python that will count how many times the decorated function was called.
    It should print the number every time the decorated function is executed.
    Each function should be counted separately.
    """
    def __call__(self, f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):

            try:
                result = f(*args, **kwargs)
            finally:
                total_count = settings.REDIS.incr(f"endpoint_usage_{f.__name__}")
                logger.info(f"Redis increment decorator for {f.__name__}: {total_count}")

            return result

        return wrapped_function
