from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from root.serializers import UserSerializer

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
                "data": UserSerializer(user, context={"request": request}).data,
            },
            status=status.HTTP_200_OK,
        )
