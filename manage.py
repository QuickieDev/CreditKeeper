# -*- coding: utf-8 -*-
"""CreditManager manage.py file.

Exports command line tools for deploying, building, testing.
"""


import bottle
from credit_manager import app
import click
import subprocess
from settings import WSGI_OPTS, DEBUG


@click.group()
def manager():
    """Base Manager instance.

     All available commands will be mounted on this object.
    """
    pass


@manager.command()
def build_docs():
    """Build Sphinx api_docs for Geotag CAAS project.
    """
    subprocess.call(['cd docs; make clean; make html; cd ..'],
                    shell=True, stdout=subprocess.PIPE)


@manager.command()
def build_js():
    """Compile Riot.js components.
    """
    subprocess.Popen(["riot", "views/components/", "static/js/components"])


@manager.command()
def watch_js():
    """Compile Riot.js components.
    """
    subprocess.Popen(["riot", "-w", "views/components/", "static/js/components"])


@manager.command()
@click.option('--host', default=WSGI_OPTS['host'], type=str, help='Set Application server host.')
@click.option('--port', default=WSGI_OPTS['port'], type=int, help='Set Application server port.')
@click.option('--server', default=WSGI_OPTS['server'], type=str, help='Set Application server wsgi container.')
@click.option('--reloader', default=WSGI_OPTS['reloader'], type=bool, help='Set Application server reloader option.')
@click.option('--debug', default=DEBUG, type=bool, help='Set Application server debug mode.')
def runserver(host, port, server, reloader, debug):
    """CreditManager app deployment.

    Args:
        host (str): Application IP or domain name.
        port (int): Application port.
        server (str): Application wsgi server alias.
        reloader (bool): Enable Application auto-reload on change.
        debug (bool): Enable Application DEBUG mode.
    """

    bottle.debug(debug)

    bottle.run(
        app=app,
        server=server,
        host=host,
        port=port,
        reloader=reloader
    )

if __name__ == '__main__':

    manager()
