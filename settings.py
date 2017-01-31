# -*- coding: utf-8 -*-
""" Credit Manager Settings module.

Provides application settings config.
"""

DEBUG = True

server_secret = '#$51365871273092qhwjdjasd913'

SERVER_HOST = 'localhost'

WSGI_OPTS = {
    'server': 'wsgiref',
    'reloader': True,
    'port': 8000,
    'host': '0.0.0.0'
}


POSTGRES = {
    'host': 'localhost',
    'port': 5432,
    'user': 'pav',
    'password': 'iverson87',
    'database': 'creditDB'
}