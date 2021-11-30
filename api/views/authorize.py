from django.conf import settings
from django.middleware import csrf
from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from administration.models import UserModel
from ..authentication import CSRFExemptUserAuthentication
from utils import errors as e
from utils.permissions import CheckAuthenticatedElseIsAnonymous


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        "refresh": str(refresh),
        "access": str(refresh.access_token),
    }


class AuthViewSet(APIView):
    authentication_classes = [CSRFExemptUserAuthentication]
    permission_classes = [CheckAuthenticatedElseIsAnonymous]

    def get(self, request, format=None):
        if request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) is not None:
            return Response(
                {
                    "status": "ok",
                    "data": {
                        "id": request.user.id,
                        "username": request.user.username,
                        "email_id": request.user.email_id,
                        "user_type": request.user.user_type,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            return e.HTTP401Response()

    def post(self, request, format=None):
        data = request.data

        try:
            username = data.get("username")
            email_id = data.get("email_id")
            password = data.get("password")

            if not password:
                return e.HTTP400Response()

            if username:
                user = authenticate(username=username, password=password)
            elif email_id:
                u = UserModel.objects.get(email_id=email_id)
                user = authenticate(username=u.username, password=password)

            else:
                return e.HTTP400Response()

            if not user:
                return e.HTTP404Response("No user found with the given credentials")

            if not user.is_active:
                return e.HTTP404Response("The Account is inactive")

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

            csrf.get_token(request)

            _response.data = {
                "id": user.id,
                "username": user.username,
                "email_id": user.email_id,
                "user_type": user.user_type,
                "authorization_token": data["access"],
                "refresh_token": data["refresh"],
            }
            _response.status_code = status.HTTP_200_OK
            return _response

        except ObjectDoesNotExist:
            return e.HTTP404Response("No user found with the given credentials")
