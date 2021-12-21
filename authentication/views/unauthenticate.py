from __future__ import annotations
from typing import TYPE_CHECKING

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

if TYPE_CHECKING:
    from django.http import HttpRequest


class UnAuthViewSet(APIView):
    def post(self, request: HttpRequest, format=None) -> Response:
        _response = Response()

        _response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        _response.delete_cookie(settings.SIMPLE_JWT["REFRESH_COOKIE"])
        _response.delete_cookie(settings.CSRF_COOKIE_NAME)

        _response.status_code = status.HTTP_205_RESET_CONTENT

        return _response
