from configurations import Configuration
from .configuration import BaseAuthConfigurationMixin, DevAuthConfigurationMixin


class Dev(DevAuthConfigurationMixin, BaseAuthConfigurationMixin, Configuration):
    DEBUG = True
    SECRET_KEY = "foobar123"
    INSTALLED_APPS = [
        'django.contrib.auth',
        'django.contrib.contenttypes',
    ] + BaseAuthConfigurationMixin.MAFIASI_AUTH_APPS
