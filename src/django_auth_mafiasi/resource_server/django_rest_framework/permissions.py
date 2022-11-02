from rest_framework.permissions import BasePermission


def get_user(request):
    return request.user


class IsStaff(BasePermission):
    """
    Grants permission if the logged-in user is considered staff

    See https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.is_staff
    """

    def has_permission(self, request, view):
        return request.user.is_staff

    def has_object_permission(self, request, view, obj):
        return request.user.is_staff


class IsSuperUser(BasePermission):
    """
    Grants permission if the logged-in user is considered a superuser

    See https://docs.djangoproject.com/en/3.1/ref/contrib/auth/#django.contrib.auth.models.User.is_superuser
    """

    def has_permission(self, request, view):
        return request.user.is_superuser

    def has_object_permission(self, request, view, obj):
        return request.user.is_superuser
