from datetime import datetime

from django.core.exceptions import ImproperlyConfigured
from django.urls import reverse
from django.conf import settings
from django.contrib import auth as django_auth
from django.shortcuts import redirect, resolve_url
from django.utils.module_loading import import_string
from oic import rndstr
from oic.oic import AuthorizationResponse

from django_auth_mafiasi.models import UserToken
from django_auth_mafiasi import auth_utils


try:
    get_user_from_id_token = import_string(
        settings.AUTH_GET_USER_FROM_ID_TOKEN_FUNCTION
    )
except ImportError as e:
    raise ImproperlyConfigured(e)


def login(request):
    client = auth_utils.get_client()
    request.session["oic_state"] = rndstr()
    request.session["oic_nonce"] = rndstr()

    auth_req = client.construct_AuthorizationRequest(
        request_args={
            "response_type": "code",
            "scope": settings.AUTH_SCOPE,
            "nonce": request.session["oic_nonce"],
            "state": request.session["oic_state"],
            "redirect_uri": request.build_absolute_uri(
                reverse("django_auth_mafiasi:login-callback")
            ),
        }
    )
    login_url = auth_req.request(client.authorization_endpoint)

    return redirect(login_url)


def login_callback(request):
    client = auth_utils.get_client()
    auth_response = client.parse_response(
        AuthorizationResponse, info=request.get_full_path(), sformat="urlencoded"
    )
    assert auth_response["state"] == request.session["oic_state"]

    now = datetime.utcnow()
    token_response = client.do_access_token_request(
        scope=settings.AUTH_SCOPE,
        state=auth_response["state"],
        request_args={
            "code": auth_response["code"],
            "redirect_uri": request.build_absolute_uri(
                reverse("django_auth_mafiasi:login-callback")
            ),
        },
        skew=30,  # allow 30-second clock screw during token validation
    )

    user = get_user_from_id_token(token_response["id_token"])
    UserToken.objects.create(
        user=user,
        access_token=token_response["access_token"],
        access_expiry=datetime.utcfromtimestamp(
            now.timestamp() + token_response["expires_in"]
        ),
        refresh_token=token_response["refresh_token"],
        refresh_expiry=datetime.utcfromtimestamp(
            now.timestamp() + token_response["refresh_expires_in"]
        ),
    )
    django_auth.login(request, user)

    return redirect(resolve_url(settings.LOGIN_REDIRECT_URL))


def logout(request):
    client = auth_utils.get_client()

    end_session_request = client.do_end_session_request(
        scope=settings.AUTH_SCOPE,
        request_args={
            "post_logout_redirect_uri": request.build_absolute_uri(
                reverse("django_auth_mafiasi:logout-callback")
            ),
            "id_token": request.session["oic_id_token"],
        },
    )

    return redirect(end_session_request.url)


def logout_callback(request):
    django_auth.logout(request)
    return redirect(resolve_url(settings.LOGOUT_REDIRECT_URL))
