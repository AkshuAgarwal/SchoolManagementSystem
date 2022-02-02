from __future__ import annotations
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from utils.py import http_responses as r
from root.models import User as UserModel

if TYPE_CHECKING:
    from rest_framework.request import Request


class PasswordValidationViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request: Request, format=None) -> Response:
        password = request.data.get("password")
        username = request.data.get("username", None)

        if not password:
            return r.HTTP400Response("Missing 'password' parameter")

        if not username:
            user = None
        else:
            try:
                user = UserModel.objects.get(username=username)
            except UserModel.DoesNotExist:
                return r.HTTP404Response("No user found with the given username")

        try:
            validate_password(password, user)
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_200_OK,
                },
                status=status.HTTP_200_OK,
            )
        except ValidationError as e:
            errors = []
            for error in e:
                errors.append(str(error))

            return Response(
                {
                    "status": "error",
                    "status_code": status.HTTP_400_BAD_REQUEST,
                    "error": {
                        "error_type": "Bad Request",
                        "error_message": "Validation Failed",
                        "errors": errors,
                    },
                },
                status=status.HTTP_400_BAD_REQUEST,
            )
