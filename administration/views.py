from django.http import JsonResponse
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .authentication import UserAuthentication
from .models import UserModel
from .serializers import UserSerializer


class UserViewSet(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        data = request.data

        try:
            if x := data.get("username"):
                user = UserModel.objects.get(username=x)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            elif x := data.get("id"):
                user = UserModel.objects.get(id=x)
                serializer = UserSerializer(user)
                return JsonResponse(serializer.data, status=status.HTTP_200_OK)

        except UserModel.DoesNotExist:
            return Response(
                {
                    "error": {
                        "type": "NotFound",
                        "message": "No user found with given credentials",
                    },
                    "status": 404,
                },
                status=status.HTTP_404_NOT_FOUND,
            )

    def post(self, request, format=None):
        FIELDS = {
            "username",
            "first_name",
            "last_name",
            "email_id",
            "user_type",
            "date_of_birth",
            "contact_no",
            "address",
            "password",
        }

        data = request.data

        if FIELDS != set(data):
            return Response(
                {
                    "error": {
                        "type": "Bad Request",
                        "message": "Required field(s) missing.",
                    },
                    "status": 400,
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if data["user_type"] not in {"s", "p", "t", "m"}:
            return Response(
                {
                    "error": {
                        "type": "Forbidden",
                        "message": "'a' (Administrator) cannot be set for normal users.",
                    },
                    "status": 403,
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        user = UserModel.objects.create_user(**data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
