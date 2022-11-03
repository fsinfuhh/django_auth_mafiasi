"""
Mixin classes when `django-configurations <https://pypi.org/project/django-configurations/>`_ is used
"""
from configurations import values


class BaseAuthConfigurationMixin:
    """
    Basic Mixin class which all django projects using this library should include
    """

    MAFIASI_AUTH_APPS = ["django_auth_mafiasi"]
    "List of apps which need to be added to django's " "`INSTALLED_APPS <https://docs.djangoproject.com/en/3.1/ref/settings/#installed-apps>`_"

    AUTH_GET_USER_FROM_ID_TOKEN_FUNCTION = (
        "django_auth_mafiasi.auth_utils.get_user_from_id_token"
    )
    "Import path of a function which is used when a user object needs to be derived from an OpenId **ID token**"

    AUTH_GET_USER_FROM_ACCESS_TOKEN_FUNCTION = (
        "django_auth_mafiasi.auth.get_user_from_access_token"
    )
    "Import path of a function which is used when a user object needs to be derived from an OpenId **access token**"

    AUTH_USER_MODEL = "django_auth_mafiasi.MafiasiAuthModelUser"
    "See `django documentation <https://docs.djangoproject.com/en/3.1/ref/settings/#auth-user-model>`_." "If you override this, your new model should inherit from MafiasiAuthModelUser"

    AUTH_SERVER = values.URLValue(
        default="https://identity.mafiasi.de/auth/realms/mafiasi"
    )
    "OpenId Issuer. This defaults to our Mafiasi server but theoretically, any OpenId Issuer can be used"

    AUTH_CLIENT_ID = values.Value(environ_required=True)
    "OpenId client id\n\n" "It needs to be manually retrieved from the OpenId server and uniquely identifies this application"

    AUTH_CLIENT_SECRET = values.SecretValue(environ_required=True)
    "OpenId client secret\n\n" "It needs to be manually retrieved from the OpenId server and authenticates this application (not the user)"

    AUTH_SCOPE = values.ListValue(default=["openid"])
    "Scopes to request when logging a user in on the OpenId provider"

    AUTH_STAFF_GROUPS = values.ListValue(default=["Server-AG"])
    "Which groups are considered to be staff (have access to the admin panel)"

    AUTH_SUPERUSER_GROUPS = values.ListValue(default=["Server-AG"])
    "Which groups are considered to be superusers (have access to everything)"

    REST_FRAMEWORK_REQUIRED_SCOPES = values.ListValue(default=["openid"])
    "Scopes to which an access token needs to have access to in order to be allowed access the an API secured by the rest framework authenticator"

    LOGIN_REDIRECT_URL = "/"
    "Where to redirect a user after successful login"

    LOGOUT_REDIRECT_URL = "/"
    "Where to redirect a user after logout"

    LOGIN_URL = "django_auth_mafiasi:login"


class DevAuthConfigurationMixin:
    """
    Development Mixin class which makes developing an application easier.

    It mainly configures the `dev-client` openid credentials and makes every user a staff and superuser.
    """

    AUTH_CLIENT_ID = values.Value(default="dev-client")
    AUTH_CLIENT_SECRET = values.Value(default="bb0c83bc-1dd9-4946-a074-d452bc1fb830")

    AUTH_STAFF_GROUPS = values.ListValue(default=["*"])
    AUTH_SUPERUSER_GROUPS = values.ListValue(default=["*"])
