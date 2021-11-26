from rest_framework import status as s
from rest_framework.response import Response


def HTTP400Response(message=None):
    return Response(
        {
            "error": {
                "type": "Bad Request",
                "message": message or "Invalid data passed",
            },
            "status": 400,
        },
        status=s.HTTP_400_BAD_REQUEST,
    )


def HTTP403Response(message=None):
    return Response(
        {
            "error": {
                "type": "Forbidden",
                "message": message or "No Access",
            },
            "status": 403,
        },
        status=s.HTTP_403_FORBIDDEN,
    )


def HTTP404Response(message=None):
    return Response(
        {
            "error": {
                "type": "NotFound",
                "message": message or "Requested data not found",
            },
            "status": 404,
        },
        status=s.HTTP_404_NOT_FOUND,
    )
