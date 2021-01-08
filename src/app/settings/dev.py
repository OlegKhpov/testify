import os

from app.settings.components.base import * # noqa
# from app.settings.components.database import * # noqa
from app.settings.components.dev_tools import * # noqa
from app.settings.components.celery import * # noqa
from app.settings.components.email import * # noqa
from app.settings.components.rest import * # noqa


# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ['SECRET_KEY']
