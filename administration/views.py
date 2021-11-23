from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view

from _utils.decorators import auth_required
from .models import UserModel


@api_view(["POST"])
@auth_required(superuser=True)
def create_user(request):
    if request.method == "POST":
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
                        "message": f"Required field(s) missing.",
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
