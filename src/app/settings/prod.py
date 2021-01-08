import os

from app.settings.components.base import * # noqa
from app.settings.components.database import * # noqa
from app.settings.components.dev_tools import * # noqa
from app.settings.components.celery import * # noqa
from app.settings.components.email import * # noqa
from app.settings.components.rest import * # noqa


DEBUG = False
SECRET_KEY = os.environ['SECRET_KEY']
STATIC_ROOT = '/var/www/testify/static'
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', '').split(':')
