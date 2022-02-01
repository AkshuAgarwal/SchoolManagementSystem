from __future__ import annotations
from typing import TYPE_CHECKING

import urllib.parse

from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from admin.permissions import IsAdmin
from utils.py import http_responses as r
from root.models import User as UserModel
from utils.py.exceptions import AlreadyExists, MissingRequiredFields

if TYPE_CHECKING:
    from rest_framework.request import Request


class UserViewSet(APIView):
    permission_classes = [IsAdmin]

    def get(self, request: Request, format=None) -> Response:
        username = request.query_params.get("username")
        email_id = request.query_params.get("email_id")
        id = request.query_params.get("id")

        try:
            if username:
                username = urllib.parse.unquote(username)
                user: UserModel = UserModel.objects.get(username=username)
            elif email_id:
                email_id = urllib.parse.unquote(email_id)
                user: UserModel = UserModel.objects.get(email_id=email_id)
            elif id:
                user: UserModel = UserModel.objects.get(id=id)
            else:
                return r.HTTP400Response("Missing 'username', 'email_id' or 'id' parameter")
        except UserModel.DoesNotExist:
            return r.HTTP404Response("No user found with the given credentials")

        return Response(
            {
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
                    "date_of_birth": user.date_of_birth.isoformat(),
                    "gender": user.gender,
                    "contact_no": user.contact_no,
                    "address": user.address,
                    "date_joined": user.date_joined.isoformat(),
                },
            },
            status=status.HTTP_200_OK,
        )

    def post(self, request: Request, format=None) -> Response:
        FIELDS = [
            "username",
            "first_name",
            "last_name",
            "email_id",
            "avatar",
            "user_type",
            "date_of_birth",
            "gender",
            "contact_no",
            "address",
            "password",
        ]
        data = {}

        for key in FIELDS:
            data[key] = request.data.get(key)

        try:
            user: UserModel = UserModel.objects.create_user(**data)
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "data": {
                        "id": user.id,
                        "username": user.username,
                        "first_name": user.first_name,
                        "last_name": user.last_name,
                        "email_id": user.email_id,
                        "avatar": request.build_absolute_uri(user.avatar.image.url) if user.avatar else None,
                        "user_type": user.user_type,
                        "date_of_birth": user.date_of_birth.isoformat(),
                        "gender": user.gender,
                        "contact_no": user.contact_no,
                        "address": user.address,
                        "date_joined": user.date_joined.isoformat(),
                    },
                },
                status=status.HTTP_201_CREATED,
            )
        except MissingRequiredFields as e:
            return r.HTTP400Response(f"Missing required fields: {', '.join(f for f in e.missing_fields)}")
        except ValidationError as e:
            return r.HTTP400Response(e.message)
        except AlreadyExists as e:
            return r.HTTP400Response(f"User already exists with given {','.join(f for f in e.colliding_fields)}")
