from django.contrib.auth import authenticate
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from administration.models import AuthorizationModel, UserModel
from utils import errors as e


class AuthViewSet(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        try:
            email_id = data.get("email_id")
            username = data.get("username")
            password = data.get("password")

            if not password:
                return e.HTTP400Response()

            if username:
                user = authenticate(username=username, password=password)
            elif email_id:
                u = UserModel.objects.get(email_id=email_id)
                user = authenticate(username=u.username, password=password)

            else:
                return e.HTTP400Response()

            if not user:
                return e.HTTP404Response("No user found with the given credentials")

            auth = AuthorizationModel.objects.get(user=user)

            return Response(
                {
                    "username": user.username,
                    "email_id": user.email_id,
                    "authorization_token": auth.authorization_token,
                },
                status=status.HTTP_200_OK,
            )

        except ObjectDoesNotExist:
            return e.HTTP404Response("No user found with the given credentials")
