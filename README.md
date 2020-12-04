# Django Auth with Mafiasi

Django authentication library for working with Mafiasi

This library is intended for people who wish to develop a new Mafiasi Service. It aims to make authentication against
mafiasi.de as easy as possible.

## How to use

- First, you need to **add the library as dependency**. We don't publish it on pypi so you will have to use a git
  dependency. See the documentation
  for [Poetry](https://python-poetry.org/docs/dependency-specification/#git-dependencies)
  , [Pipenv](https://pipenv-fork.readthedocs.io/en/latest/basics.html#a-note-about-vcs-dependencies) or
  plain [requirements.txt](https://stackoverflow.com/questions/16584552/how-to-state-in-requirements-txt-a-direct-github-source)
  syntax.

  The relevant repository is the one
  at [git.mafiasi.de/mafiasi-ag/django_auth_mafiasi](https://git.mafiasi.de/mafiasi-ag/django_auth_mafiasi).

- Next, **confiugre your Django application** ([docs](https://docs.djangoproject.com/en/3.1/topics/settings/)).

    - If you use the *django-configurations* package, you can simply
      the `django_auth_mafiasi.configuration.BaseAuthConfigurationMixin` to your configuration class:
      ```python
      # settings.py
      
      from django_auth_mafiasi.configuration import BaseAuthConfigurationMixin
    
      class MyConfig(BaseAuthConfigurationMixin, Configuration):
          INSTALLED_APPS = [
            …
          ] + BaseAuthConfigurationMixin.MAFIASI_AUTH_APPS
      ```

      A development configuration mixin exists as well. This is configured to authorize every mafiasi user and uses
      the *dev-client* for mafiasi-identity connections.

    - If you don't use *django-configurations* you will have to define the settings listed on the
      `BaseAuthConfigurationMixin` class
      from [configuration.py](https://git.mafiasi.de/mafiasi-ag/django_auth_mafiasi/src/branch/master/django_auth_mafiasi/configuration.py)
      in your settings.py file manually. Be sure to also add the defined apps to your *INSTALLED_APPS*:
      ```python
      # settings.py
      
      AUTH_GET_USER_FUNCTION = "django_auth_mafiasi.auth:get_user_from_token"
      AUTH_USER_MODEL = "django_auth_mafiasi.MafiasiAuthModelUser"
  
      AUTH_SERVER = "https://identity.mafiasi.de/auth/realms/mafiasi"
      AUTH_CLIENT_ID = os.environ.get("DJANGO_AUTH_CLIENT_ID")
      AUTH_CLIENT_SECRET = os.environ.get("DJANGO_AUTH_CLIENT_SECRET")
      AUTH_SCOPE = ["openid"]
  
      AUTH_STAFF_GROUPS = ["Mafiasi-AG"]
      AUTH_SUPERUSER_GROUPS = ["Server-AG"]
      
      INSTALLED_APPS = [
          …,
          "django_auth_oidc",
          "django_auth_mafiasi",
      ]
      ```

- Finally you need to **include routes** in your *urls.py* file:
  ```python
  # ursl.py
  from django.urls import include, path
  
  urlpatterns = [
    …,
    path('', include('django_auth_mafiasi.urls')),
  ]
  ```
