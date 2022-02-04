from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from utils.py import http_responses as r
from root.models import Subject as SubjectModel
from root.serializers import SubjectSerializer

if TYPE_CHECKING:
    from rest_framework.request import Request


class SubjectViewSet(APIView):
    def get(self, request: Request, format=None) -> Response:
        id = request.query_params.get("id")
        name = request.query_params.get("name")
        code = request.query_params.get("code")

        try:
            if id:
                subject: SubjectModel = SubjectModel.objects.get(id=id)
            else:
                if name and code:
                    subject: SubjectModel = SubjectModel.objects.get(name=name, code=code)
                else:
                    raise r.HTTP400Response("Missing 'id', or 'name' and 'code' parameters")
        except SubjectModel.DoesNotExist:
            return r.HTTP404Response("No subject found with the given data")

        return Response(
            {
                "status": "success",
                "status_code": status.HTTP_200_OK,
                "data": SubjectSerializer(subject, context={"request": request}, fields={"id", "name", "code"}).data,
            },
            status=status.HTTP_200_OK,
        )
