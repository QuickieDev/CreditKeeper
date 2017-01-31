# -*- coding: utf-8 -*-
"""`credit_manager.uls` module.

Provides app routes registry.
"""
from bottle import static_file
from bottle_neck import Router
from credit_manager.handlers import CalendarHandler, LoginHandler, LogoutHandler, APIHandler


#  server static files

def static(filename):
    return static_file(filename, root='static')


router = Router()
router.register_handler(CalendarHandler, '/')
router.register_handler(APIHandler, '/api')
router.register_handler(LoginHandler, '/login')
router.register_handler(LogoutHandler, '/logout')
router.register_handler(static, '/static/<filename:path>')
