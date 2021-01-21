from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from py_jwt_verifier import PyJwtVerifier, PyJwtException
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.request import Request

from django_auth_mafiasi.auth import get_user_from_access_token


class OpenIdAccessTokenAuthentication(BaseAuthentication):
    """
    Authenticates users based on an OpenId access token in `Authorization: Bearer <…>` header
    """
    def authenticate(self, request: Request):
        scheme, token = str(request.headers["authorization"]).split(" ", 1)
        if scheme.lower() != "bearer":
            return None

        try:
            decoded_token = PyJwtVerifier(token, iss=settings.AUTH_SERVER, cache_enabled=False).decoded_payload
            user = get_user_from_access_token(decoded_token)
            return user, decoded_token
        except PyJwtException as e:
            raise AuthenticationFailed(detail=str(e))
