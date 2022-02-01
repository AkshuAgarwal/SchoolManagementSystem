from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

if TYPE_CHECKING:
    from rest_framework.request import Request

    from root.models import User as UserModel


class MeViewSet(APIView):
    def get(self, request: Request, format=None) -> Response:
        user: UserModel = request.user

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
