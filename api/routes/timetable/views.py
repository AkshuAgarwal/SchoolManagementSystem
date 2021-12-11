import datetime
from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import TimetableModel
from .serializers import TimetableSerializer
from authentication.authentication import UserAuthentication
from utils import errors as e
from utils.permissions import TimetableRoutePermission


class TimeTableView(APIView):
    permission_classes = [TimetableRoutePermission]
    authentication_classes = [UserAuthentication]

    def get(self, request, format=None):
        date = datetime.datetime.strptime(request.data["date"], "%d/%m/%Y").date()
        grade = request.data["grade"]
        timetable = TimetableModel.objects.filter(date=date, grade=grade)

        if not timetable:
            return e.HTTP404Response()

        serializer = TimetableSerializer(timetable)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request, format=None):
        data = request.data

        data["date"] = datetime.datetime.strptime(data["date"], "%d/%m/%Y").date()
        try:
            timetable = TimetableModel.objects.create(**data)
        except ValidationError as exc:
            return e.HTTP400Response(f"Timetable for data: {exc} already exists")

        serializer = TimetableSerializer(timetable)
        return Response(
            {
                "status": "ok",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
