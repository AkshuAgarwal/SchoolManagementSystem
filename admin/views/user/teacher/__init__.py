from __future__ import annotations
from typing import TYPE_CHECKING

from django.core.exceptions import ValidationError

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from api.permissions import IsStaff
from utils.py import http_responses as r
from root.serializers import TeacherSerializer
from root.models import User as UserModel, Teacher as TeacherModel
from utils.py.exceptions import AlreadyExists, MissingRequiredFields

if TYPE_CHECKING:
    from rest_framework.request import Request


class TeacherViewSet(APIView):
    permission_classes = [IsStaff]

    def post(self, request: Request, format=None) -> Response:
        FIELDS = [
            "teacher",
            "subject",
            "year_of_joining",
            "salary",
            "classes",
            "owns_class",
        ]
        data = {}

        for key in FIELDS:
            data[key] = request.data.get(key)

        if isinstance(data["teacher"], str):
            data["teacher"] = UserModel.objects.get(username=data["teacher"])

        try:
            teacher: TeacherModel = TeacherModel.objects.create(**data)
            return Response(
                {
                    "status": "success",
                    "status_code": status.HTTP_201_CREATED,
                    "data": TeacherSerializer(teacher, context={"request": request}).data,
                },
                status=status.HTTP_201_CREATED,
            )
        except MissingRequiredFields as e:
            return r.HTTP400Response(f"Missing required fields: {', '.join(f for f in e.missing_fields)}")
        except ValidationError as e:
            return r.HTTP400Response(e.message)
        except AlreadyExists as e:
            return r.HTTP400Response(f"Teacher already exists with given data")
