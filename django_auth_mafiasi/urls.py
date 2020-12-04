from django.urls import path, include

urlpatterns = [
    path("auth/", include("django_auth_oidc.urls")),
]
