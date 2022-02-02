from __future__ import annotations
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from admin.permissions import IsStaff
from utils.py import http_responses as r
from root.serializers import ParentSerializer
from root.models import User as UserModel, Parent as ParentModel
from utils.py.exceptions import AlreadyExists, MissingRequiredFields

if TYPE_CHECKING:
    from rest_framework.request import Request


class ParentViewSet(APIView):
    permission_classes = [IsStaff]

    def post(self, request: Request, format=None) -> Response:
        FIELDS = [
            "parent",
        ]
        data = {}

        for key in FIELDS:
            data[key] = request.data.get(key)

        if isinstance(data["parent"], str):
            data["parent"] = UserModel.objects.get(username=data["parent"])

        try:
            parent: ParentModel = ParentModel.objects.create(**data)
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "data": ParentSerializer(parent, context={"request": request}).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except MissingRequiredFields as e:
            return r.HTTP400Response(f"Missing required fields: {', '.join(f for f in e.missing_fields)}")
        except ValidationError as e:
            return r.HTTP400Response(e.message)
        except AlreadyExists as e:
            return r.HTTP400Response(f"Parent already exists with given data")
