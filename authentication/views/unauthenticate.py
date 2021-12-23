from __future__ import annotations
from typing import TYPE_CHECKING

from django.conf import settings

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from utils import http_responses as r

if TYPE_CHECKING:
    from django.http import HttpRequest


class UnAuthViewSet(APIView):
    def post(self, request: HttpRequest, format=None) -> Response:
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"])
        if not refresh_token:
            refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return r.HTTP400Response("Missing 'refresh_token'")

        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
        except TokenError:
            pass

        _response = Response()

        _response.delete_cookie(settings.SIMPLE_JWT["AUTH_COOKIE"])
        _response.delete_cookie(settings.SIMPLE_JWT["REFRESH_COOKIE"])
        _response.delete_cookie(settings.CSRF_COOKIE_NAME)

        _response.status_code = status.HTTP_205_RESET_CONTENT
        return _response
