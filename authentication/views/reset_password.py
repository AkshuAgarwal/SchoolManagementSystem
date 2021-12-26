from __future__ import annotations
from typing import Any, TYPE_CHECKING

from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from root.models import User as UserModel
from ..backend import PasswordResetTokenBackend
from utils import http_responses as r

if TYPE_CHECKING:
    from django.http import HttpRequest


class ResetPasswordViewSet(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def __init__(self, **kwargs: Any) -> None:
        super().__init__(**kwargs)

        # Password reset token backend
        self.pwt_backend = PasswordResetTokenBackend()

    def post(self, request: HttpRequest, format=None):
        data = request.data

        username = data.get("username")
        email_id = data.get("email_id")

        try:
            if username:
                user: UserModel = UserModel.objects.get(username=username)
            elif email_id:
                user: UserModel = UserModel.objects.get(email_id=email_id)
            else:
                return r.HTTP400Response("Missing 'username' or 'email_id'")
        except UserModel.DoesNotExist:
            return r.HTTP404Response("No user found with the given credentials")

        response = self.pwt_backend.create(user)

        if isinstance(response, bool):
            return r.HTTP403Response("An unexpired token is already associated with the user")

        token, generation_time, lifetime = response

        return Response(
            {
                "status": "success",
                "status_code": 200,
                "data": {
                    "username": user.username,
                    "email_id": user.email_id,
                    "token": {
                        "token": token,
                        "lifetime": lifetime.seconds,
                        "generated_at": generation_time.isoformat(),
                    },
                },
            },
            status=status.HTTP_200_OK,
        )

    def patch(self, request: HttpRequest, format=None):
        data = request.data

        username = data.get("username")
        token = data.get("token")
        new_password = data.get("new_password")

        if not username:
            return r.HTTP400Response("Missing username")
        if not token:
            return r.HTTP400Response("Missing validation token")
        if not new_password:
            return r.HTTP400Response("Missing new password")

        try:
            user: UserModel = UserModel.objects.get(username=username)
        except UserModel.DoesNotExist:
            return r.HTTP400Response("No user found with the given username")

        validated = self.pwt_backend.validate(username=user.username, token=token)

        if validated is None:
            return r.HTTP400Response("Token expired or not found")
        elif validated is False:
            return r.HTTP400Response("Token does not match")
        else:  # validation successful
            self.pwt_backend.delete(user.username)  # delete the token since it's no longer needed (and shouldn't be used more than once)
            try:
                validate_password(new_password, user)
            except ValidationError as e:
                return r.HTTP400Response(e.message)
            user.set_password(new_password)
            user.save()

            return Response(
                {
                    "status": "success",
                    "status_code": 200,
                },
                status=status.HTTP_200_OK,
            )
