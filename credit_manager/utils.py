# -*- coding: utf-8 -*-
"""`credit_manager.utils` module.

Provides app common utilities.
"""

from functools import wraps
from bottle import redirect, request
from settings import server_secret
from json import JSONDecodeError


def json_required(callback):
    """Web handler decorator that ensures request data is JSON valid string.

    Args:
        callback (object): Web handler callable.
    """

    @wraps(callback)
    def _wrapper(*args, **kwargs):
        try:
            request.json

        except JSONDecodeError:
            #  set Content-type to JSON
            self.response.content_type = 'application/json'
            self.response._status_line = '400 Bad Request'

            return {"Error": "Invalid JSON Data format."}

        return callback(*args, **kwargs)

    return _wrapper


def login_required(redirect_url='/'):
    """Login required decorator, for detecting authorized requests.

     Args:
         redirect_url (str): The URL to redirect unauthorized requests (i.e login view).
    """

    def wrapper(callback):
        @wraps(callback)
        def _wrapper(*args, **kwargs):
            if request.get_cookie('__utmb', secret=server_secret):
                return callback(*args, **kwargs)

            redirect(redirect_url + '?next=' + request.path)

        return _wrapper

    return wrapper
