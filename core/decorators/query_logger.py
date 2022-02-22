import logging
from functools import wraps
from django.db import connection, reset_queries


logger = logging.getLogger("ergon_test")


class LastQueryLogger:

    def __call__(self, f):
        @wraps(f)
        def wrapped_function(*args, **kwargs):
            # initialize something before the function

            result = f(*args, **kwargs)

            # take the action after the execution
            for q in connection.queries:
                sql = q.get('sql')
                time = q.get('time')
                logger.info(f"time taken: {time} query: {sql}")

            reset_queries()
            return result

        return wrapped_function
