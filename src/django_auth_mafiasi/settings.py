#
# This settings file is only used during development so that manage.py can generate migrations.
# It is not shipped with the built django_auth_mafiasi package.
#
from configurations import Configuration
from .configuration import BaseAuthConfigurationMixin, DevAuthConfigurationMixin


class Dev(DevAuthConfigurationMixin, BaseAuthConfigurationMixin, Configuration):
    DEBUG = True
    SECRET_KEY = "foobar123"
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ] + BaseAuthConfigurationMixin.MAFIASI_AUTH_APPS
