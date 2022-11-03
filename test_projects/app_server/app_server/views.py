from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse


@login_required
def index(request: HttpRequest) -> HttpResponse:
    request.user.refresh_from_mafiasi_identity()
    request.user.full_clean()
    request.user.save()
    return JsonResponse(
        data={
            "is_authenticated": request.user.is_authenticated,
            "email": request.user.email,
            "username": request.user.username,
            "first_name": request.user.first_name,
            "last_name": request.user.last_name,
            "display_name": request.user.display_name,
            "is_staff": request.user.is_staff,
            "is_superuser": request.user.is_superuser,
        }
    )
