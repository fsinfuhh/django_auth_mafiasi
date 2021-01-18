from configurations import values


class BaseAuthConfigurationMixin:
    MAFIASI_AUTH_APPS = ["django_auth_oidc", "django_auth_mafiasi"]

    AUTH_GET_USER_FUNCTION = "django_auth_mafiasi.auth:get_user_from_token"
    AUTH_USER_MODEL = "django_auth_mafiasi.MafiasiAuthModelUser"

    AUTH_SERVER = values.URLValue(default="https://identity.mafiasi.de/auth/realms/mafiasi")
    AUTH_CLIENT_ID = values.Value(environ_required=True)
    AUTH_CLIENT_SECRET = values.SecretValue(environ_required=True)
    AUTH_SCOPE = values.ListValue(default=["openid"])

    AUTH_STAFF_GROUPS = values.ListValue(default=["Mafiasi-AG"])
    AUTH_SUPERUSER_GROUPS = values.ListValue(default=["Server-AG"])


class DevAuthConfigurationMixin:
    AUTH_CLIENT_ID = values.Value(default="dev-client")
    AUTH_CLIENT_SECRET = values.Value(default="bb0c83bc-1dd9-4946-a074-d452bc1fb830")

    AUTH_STAFF_GROUPS = values.ListValue(default=["*"])
    AUTH_SUPERUSER_GROUPS = values.ListValue(default=["*"])

