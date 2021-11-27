from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from .authentication import UserAuthentication
from .models import UserModel
from .serializers import UserSerializer
from utils import errors as e


class UsersViewSet(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAdminUser]

    def get(self, request, format=None):
        username = request.GET.get("username", None)
        id = request.GET.get("id", None)

        if username and id:
            return e.HTTP400Response('Cannot pass both "username" and "id" parameter')

        if not username and not id:
            return e.HTTP400Response('One of "username" or "id" should be passed')

        try:
            if username:
                user = UserModel.objects.get(username=username)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            if id:
                user = UserModel.objects.get(id=id)
                serializer = UserSerializer(user)
                return Response(serializer.data, status=status.HTTP_200_OK)

            return e.HTTP400Response()

        except ObjectDoesNotExist:
            return e.HTTP404Response("No user found with given credentials")

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
            return e.HTTP400Response()

        if data["user_type"] not in {"s", "p", "t", "m"}:
            return e.HTTP403Response('"a" (Administrator) cannot be set for normal users')

        user = UserModel.objects.create_user(**data)
        serializer = UserSerializer(user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
