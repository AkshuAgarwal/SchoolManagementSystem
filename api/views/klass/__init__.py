from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.py import http_responses as r
from root.models import Class as ClassModel
from root.serializers import ClassSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class ClassViewSet(APIView):
    def get(self, request: Request, format=None) -> Response:
        id = request.query_params.get("id")
        grade = request.query_params.get("grade")
        section = request.query_params.get("section")

        try:
            if id:
                klass: ClassModel = ClassModel.objects.get(id=id)
            else:
                if grade and section:
                    klass: ClassModel = ClassModel.objects.get(grade=grade, section=section)
                else:
                    raise r.HTTP400Response("Missing 'id', or 'grade' and 'section' parameters")
        except ClassModel.DoesNotExist:
            return r.HTTP404Response("No class found with the given data")

        return Response(
            {
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "data": ClassSerializer(klass, context={"request": request}, fields={"id", "grade", "section"}).data,
            },
            status=status.HTTP_200_OK,
        )
