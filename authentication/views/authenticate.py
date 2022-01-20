from __future__ import annotations
from typing import TypedDict, TYPE_CHECKING

from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.contrib.auth.models import update_last_login

from rest_framework import status, HTTP_HEADER_ENCODING
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.token_blacklist.models import OutstandingToken

from ..authentication import CSRFExemptAuthentication
from utils.py import http_responses as r

if TYPE_CHECKING:
    from rest_framework.request import Request
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

    def get(self, request: Request, format=None) -> Response:
        if request.user.is_authenticated:
            outstanding_token = OutstandingToken.objects.filter(user=request.user).order_by("-created_at")[0]
            refresh = RefreshToken(outstanding_token.token)

            # `RefreshToken.access_token` generates a new token instead of getting the old one
            # For returning original token, we need to fetch it from Cookies or Headers
            def get_access_token():
                header = request.META.get(settings.SIMPLE_JWT["AUTH_HEADER_NAME"])
                if isinstance(header, str):
                    header = header.encode(HTTP_HEADER_ENCODING)

                if header is None:
                    access = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"])
                else:
                    access = header.split()[1]
                return access

            access = get_access_token()

            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_200_OK,
                    "data": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "first_name": request.user.first_name,
                        "last_name": request.user.last_name,
                        "email_id": request.user.email_id,
                        "avatar": request.build_absolute_uri(request.user.avatar.image.url)
                        if request.user.avatar
                        else None,
                        "user_type": request.user.user_type,
                        "access_token": str(access),
                        "refresh_token": str(refresh),
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return r.HTTP401Response()

    def post(self, request: Request, format=None) -> Response:
        if TYPE_CHECKING:
            user: UserModel

        username = request.data.get("username")
        email_id = request.data.get("email_id")
        password = request.data.get("password")

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

        csrf.get_token(request)

        _response.set_cookie(
            key=settings.SIMPLE_JWT["AUTH_COOKIE"],
            value=data["access"],
            max_age=settings.SIMPLE_JWT["ACCESS_TOKEN_LIFETIME"].total_seconds(),
            path=settings.SIMPLE_JWT["AUTH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["AUTH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        )
        _response.set_cookie(
            key=settings.SIMPLE_JWT["REFRESH_COOKIE"],
            value=data["refresh"],
            max_age=settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds(),
            path=settings.SIMPLE_JWT["REFRESH_COOKIE_PATH"],
            secure=settings.SIMPLE_JWT["REFRESH_COOKIE_SECURE"],
            httponly=settings.SIMPLE_JWT["REFRESH_COOKIE_HTTP_ONLY"],
            samesite=settings.SIMPLE_JWT["REFRESH_COOKIE_SAMESITE"],
        )

        _response.data = {
            "status": "success",
            "status_code": status.HTTP_200_OK,
            "data": {
                "id": user.id,
                "username": user.username,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "email_id": user.email_id,
                "avatar": request.build_absolute_uri(user.avatar.image.url) if user.avatar else None,
                "user_type": user.user_type,
                "access_token": data["access"],
                "refresh_token": data["refresh"],
            },
        }

        _response.status_code = status.HTTP_200_OK

        update_last_login(None, user)

        return _response
