from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.module_loading import import_string
from rest_framework.authentication import BaseAuthentication
from py_jwt_verifier import PyJwtVerifier, PyJwtException
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

try:
    from .openapi import *
except ImportError:
    # this was probably because drf-spectacular is not installed
    # we can ignore the error because we don't need to provide any metadata to drf-spectacula if it is not used
    pass


try:
    get_user_from_access_token = import_string(settings.AUTH_GET_USER_FROM_ACCESS_TOKEN_FUNCTION)
except ImportError as e:
    raise ImproperlyConfigured(e)


class OpenIdAccessTokenAuthentication(BaseAuthentication):
    """
    Authenticates users based on an OpenId access token in `Authorization: Bearer <…>` header
    """
    def authenticate(self, request: Request):
        scheme, token = str(request.headers["authorization"]).split(" ", 1)
        if scheme.lower() != "bearer":
            return None

        decoded_token = self._verify_token(token)
        user = get_user_from_access_token(decoded_token)
        return user, decoded_token

    @staticmethod
    def _verify_token(token: str) -> dict:
        """
        Verify the given JWT token for standardized validity (i.e. expiry and matching issuer) as well as
        application constraints (i.e. required scopes)

        :param token: The encoded JWT token
        :return: The decoded and validated JWT token payload
        """
        try:
            # validate for standardized validity
            decoded_token = PyJwtVerifier(token, iss=settings.AUTH_SERVER, cache_enabled=False).decoded_payload
        except PyJwtException as e:
            raise AuthenticationFailed(detail=str(e))

        # validate required scopes
        token_scopes = decoded_token["scope"].split(" ")
        missing_scopes = [i for i in settings.REST_FRAMEWORK_AUTH["REQUIRED_SCOPES"] if i not in token_scopes]
        if len(missing_scopes) > 0:
            raise AuthenticationFailed(detail=f"token is missing scopes {missing_scopes} which are required "
                                              f"for accessing this application")

        return decoded_token
