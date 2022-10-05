# -*- copyright -*-

# Dependencies
from functools import partial, wraps

# decorators.py
# Author: Nicolas Delgado


def use_headers(func=None, *, allowed_methods=["GET"]):
    if not func:
        return partial(use_headers, allowed_methods=allowed_methods)

    @wraps(func)
    def wrapper(*args, **kwargs):
        headers = {
            "Access-Control-Allow-Origin": "*",
            "Access-Control-Allow-Methods": ",".join(allowed_methods),
            "Access-Control-Allow-Headers": "Content-Type,Authorization",
            "Access-Control-Max-Age": "3600",
        }

        kwargs["headers"] = headers
        return func(*args, **kwargs)

    return wrapper
