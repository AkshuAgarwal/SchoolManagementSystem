from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from .models import ContactMessageModel
from .serializers import ContactMessageSerializer
from utils import errors as e


class ContactMessagesView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, format=None):
        data = request.data

        VALID_KEYS = {"first_name", "last_name", "email_id", "message"}

        for key in set(data):
            if key not in VALID_KEYS:
                return e.HTTP400Response("One or more fields are invalid")

        first_name = data.get("first_name", None)
        last_name = data.get("last_name", "")
        email_id = data.get("email_id", None)
        message = data.get("message", None)

        if not all([first_name, email_id, message]):
            return e.HTTP400Response("One of the required fields is missing")

        contact_message = ContactMessageModel.objects.create(
            first_name=first_name,
            last_name=last_name,
            email_id=email_id,
            message=message,
        )
        serializer = ContactMessageSerializer(contact_message)
        return Response(
            {
                "status": "ok",
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED,
        )
