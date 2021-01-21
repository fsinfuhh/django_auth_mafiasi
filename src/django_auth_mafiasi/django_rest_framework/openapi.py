from drf_spectacular.extensions import OpenApiAuthenticationExtension
from django.conf import settings


class OpenIdAccessTokenAuthenticationExtension(OpenApiAuthenticationExtension):
    """
    Provides metadata for srf-spectacular based OpenApi schema generation
    """
    target_class = "django_auth_mafiasi.django_rest_framework.authentication.OpenIdAccessTokenAuthentication"
    name = "openIdAccessTokenAuth"

    def get_security_requirement(self, auto_schema):
        return super().get_security_requirement(auto_schema)

    def get_security_definition(self, auto_schema):
        return {
            "type": "http",
            "description": "Mafiasi OpenId access token retrieved when logging in with MafiasiIdentity",
            "scheme": "Bearer",
            "bearerFormat": "JWT",
        }


