# -*- coding: utf-8 -*-
"""`credit_manager.handlers` module.

Provides app web handlers.
"""

from bottle import jinja2_template, static_file, redirect, request
from bottle_neck import BaseHandler
from credit_manager.utils import login_required, json_required
from credit_manager.models import CreditModel
from credit_manager.errors import ModelError
from settings import server_secret, SERVER_HOST
import time
import ujson


class LogoutHandler(BaseHandler):
    """Logout page handler.
    """

    def get(self):

        page = self.request.query.smart_filters().get('current', '/')

        self.response.set_cookie(
            '__utmb',
            '',
            secret=server_secret,
            expires=time.time() - (3600 * 24 * 365),
            domain=SERVER_HOST,
            path='/'
        )

        return redirect('/login?next={}'.format(page))


class LoginHandler(BaseHandler):
    """Login page web handler.
    """

    @staticmethod
    def _authenticate(username, password):
        return username == password == 'admin'

    def get(self):
        """Return login form
        """
        next_page = self.request.query.smart_filters().get('next') or '/calendar'
        return jinja2_template('login.html', {'next_url': next_page})

    def post(self):
        username = self.request.forms.get('username') or ''
        password = self.request.forms.get('password') or ''

        next_page = self.request.query.smart_filters().get('next')

        if not self._authenticate(username, password):
            return self.template(
                'login.html',
                {"errors": "Unable to login with provided credentials", "next_url": next_page}
            )

        self.response.set_cookie(
            '__utmb',
            'credit_admin',
            secret=server_secret,
            expires=time.time() + (3600 * 24 * 365),
            domain=SERVER_HOST,
            path='/'
        )

        redirect(next_page or '/calendar')


class CalendarHandler(BaseHandler):
    """Home page web handler.
    """

    @login_required('/login')
    def get(self):
        return jinja2_template('calendar.html', {'current': self.request.path, 'active': 'calendar'})


class APIHandler(BaseHandler):
    """API web handler.
    """
    filters = lambda: request.query.smart_filters()
    model = CreditModel

    def get(self, uid=None):
        """Retrieve Credit Events.
        """

        if uid:

            if self.model.exists(uid):

                credit_record = self.model.retrieve(uid)
                return credit_record

            self.response.content_type = 'application/json'
            self.response._status_line = '404 Not Found'
            return ujson.dumps({"Error": "Credit {} does not exist!".format(uid)})

        # get Filters

        api_params = self.filters()

        # execute query

        credit_records = self.model.list(
            start=api_params.get('start'),
            stop=api_params.get('stop')
        )

        #  set Content-type to JSON
        self.response.content_type = 'application/json'

        return ujson.dumps(credit_records)

    @json_required
    def post(self):
        """Create Credit events.
        """
        credit = self.model.create(self.request.json)

        return credit

    @json_required
    def put(self, uid):
        """Update Credit Events.
        """

        if not self.model.exists(uid):

            self.response.content_type = 'application/json'
            self.response._status_line = '404 Not Found'

            return ujson.dumps({"Error": "Credit {} does not exist!".format(uid)})

        credit_data = self.request.json

        credit_record = self.model.update(uid, credit_data)

        return credit_record

    def delete(self, uid):
        """Delete Credit Event.
        """
        if not self.model.exists(uid):

            self.response.content_type = 'application/json'
            self.response._status_line = '404 Not Found'

            return ujson.dumps({"Error": "Credit {} does not exist!".format(uid)})

        credit_record = self.model.delete(uid)

        return credit_record
