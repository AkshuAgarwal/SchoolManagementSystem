from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken

from ..authentication import CSRFExemptAuthentication
from utils import http_responses as r

if TYPE_CHECKING:
    from django.http import HttpRequest
    from root.models import User as UserModel


class TokenDict(TypedDict):
    refresh: str
    access: str


def get_tokens_for_user(user: UserModel) -> TokenDict:
    refresh = RefreshToken.for_user(user)
    return TokenDict(refresh=str(refresh), access=str(refresh.access_token))


class AuthViewSet(APIView):
    authentication_classes = [CSRFExemptAuthentication]
    permission_classes = [AllowAny]

    def get(self, request: HttpRequest, format=None) -> Response:
        if request.user.is_authenticated:
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)

    def post(self, request: HttpRequest, format=None) -> Response:
        if TYPE_CHECKING:
            user: UserModel

        data = request.data

        username = data.get("username")
        email_id = data.get("email_id")
        password = data.get("password")

        if not password:
            return r.HTTP400Response("Missing 'password'")

        if username:
            user = authenticate(username=username, password=password)
        elif email_id:
            user = authenticate(email_id=email_id, password=password)
        else:
            return r.HTTP400Response("Missing 'username' or 'email_id'")

        if not user:
            return r.HTTP404Response("No user found with the given credentials")

        data = get_tokens_for_user(user)

        _response = Response()

        _response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=data["access"],
            expires=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"],
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        _response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE"],
            value=data["refresh"],
            expires=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"],
            path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["REFRESH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["REFRESH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["REFRESH_COOKIE_SAMESITE"],
        )

        csrf.get_token(request)

        _response.data = {
            "status": "success",
            "status_code": 200,
            "data": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id,
                "avatar": request.build_absolute_uri(user.avatar.image.url),
                "user_type": user.user_type,
                "access_token": data["access"],
                "refresh_token": data["refresh"],
            },
        }

        _response.status_code = status.HTTP_200_OK
        return _response
