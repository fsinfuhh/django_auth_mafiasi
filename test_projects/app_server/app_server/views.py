from django.contrib.auth.decorators import login_required
from django.http.request import HttpRequest
from django.http.response import HttpResponse, JsonResponse


@login_required
def index(request: HttpRequest) -> HttpResponse:
    return JsonResponse(data={
        "is_authenticated": request.user.is_authenticated,
        "email": request.user.email,
    })
