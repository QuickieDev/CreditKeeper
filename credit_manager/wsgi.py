# -*- coding: utf-8 -*-
"""`credit_manager.wsgi` module.

Provides app plugins and route registry.
"""


import bottle
from bottle_neck import StripPathMiddleware, Router
from bottle_smart_filters import SmartFiltersPlugin
from credit_manager.urls import router

app = StripPathMiddleware(bottle.Bottle())
app.install(SmartFiltersPlugin())

router.mount(app)
