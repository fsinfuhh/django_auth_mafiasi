from django.urls import path
from django.views.generic import RedirectView
from django_auth_mafiasi.app_server import views

app_name = "django_auth_mafiasi"
urlpatterns = [
    path("", RedirectView.as_view(url="./login")),
    path("login", views.login, name="login"),
    path("callback", views.login_callback, name="login-callback"),
    path("logout", views.logout, name="logout"),
    path("logout-callback", views.logout_callback, name="logout-callback"),
]
