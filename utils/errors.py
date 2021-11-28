from rest_framework import status as s
from rest_framework.response import Response


def HTTP400Response(message=None):
    return Response(
        {
            "detail": {
                "error_type": "Bad Request",
                "error_message": message or "Invalid data passed",
            },
            "status": 400,
        },
        status=s.HTTP_400_BAD_REQUEST,
    )


def HTTP401Response(message=None):
    return Response(
        {
            "detail": {
                "error_type": "Unauthorized",
                "error_message": message or "Unauthorized",
            },
            "status": 401,
        },
        status=s.HTTP_401_UNAUTHORIZED,
    )


def HTTP403Response(message=None):
    return Response(
        {
            "detail": {
                "error_type": "Forbidden",
                "error_message": message or "No Access",
            },
            "status": 403,
        },
        status=s.HTTP_403_FORBIDDEN,
    )


def HTTP404Response(message=None):
    return Response(
        {
            "detail": {
                "error_type": "NotFound",
                "error_message": message or "Requested data not found",
            },
            "status": 404,
        },
        status=s.HTTP_404_NOT_FOUND,
    )
