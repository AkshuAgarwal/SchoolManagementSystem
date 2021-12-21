from __future__ import annotations
from typing import TYPE_CHECKING

from django.conf import settings
from django.test.client import RequestFactory

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import token_refresh

from utils import http_responses as r

if TYPE_CHECKING:
    from django.http import HttpRequest


class RefreshTokenViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: HttpRequest, format=None) -> Response:
        refresh_token = request.COOKIES.get(settings.SIMPLE_JWT["REFRESH_COOKIE"])
        if not refresh_token:
            refresh_token = request.data.get("refresh_token")

        if not refresh_token:
            return r.HTTP400Response("Missing 'refresh_token'")

        # simplejwt token_refresh view don't support cookie based refresh token fetching, so we're gonna fake it
        _fakefactory = RequestFactory()
        _fakerequest = _fakefactory.post("/", data={"refresh": refresh_token}, content_type="application/json")

        _fakeresponse = token_refresh(_fakerequest)
        if _fakeresponse.status_code == 200:
            return Response(
                {
                    "status": "success",
                    "status_code": 201,
                    "data": {
                        "access_token": _fakeresponse.data["access"],
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        elif _fakeresponse.status_code == 401:
            return r.HTTP401Response("Refresh token is invalid or expired")
        else:
            return r.HTTP500Response()
