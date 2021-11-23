import functools

from rest_framework.response import Response
from rest_framework import status

from administration.models import UserModel


def auth_required(superuser: bool = True):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(request, *args, **kwargs):
            auth_token = request.headers.get("X-Authorization-Token")
            if auth_token is not None:
                try:
                    if len(splitted := auth_token.split(" ")) == 2:
                        keyword, token = splitted
                    else:
                        return Response(
                            {
                                "error": {
                                    "type": "Unauthorized",
                                    "message": "Invalid Authorization Token",
                                },
                                "status": 401,
                            },
                            status=status.HTTP_401_UNAUTHORIZED,
                        )
                    if keyword == "Bearer":
                        user = UserModel.objects.get(authorization_token=token)
                    else:
                        return Response(
                            {
                                "error": {
                                    "type": "Bad Request",
                                    "message": "Invalid Token type passed.",
                                },
                                "status": 400,
                            },
                            status=status.HTTP_400_BAD_REQUEST,
                        )
                    if superuser is True:
                        if user.is_superuser is True:
                            return func(request, *args, **kwargs)
                        else:
                            return Response(
                                {
                                    "error": {
                                        "type": "Forbidden",
                                        "zmessage": "This route is only accessible to superusers.",
                                    },
                                    "status": 403,
                                },
                                status=status.HTTP_403_FORBIDDEN,
                            )
                    return func(request, *args, **kwargs)
                except UserModel.DoesNotExist:
                    return Response(
                        {
                            "error": {
                                "type": "Unauthorized",
                                "message": "Invalid Authorization Token",
                            },
                            "status": 401,
                        },
                        status=status.HTTP_401_UNAUTHORIZED,
                    )
            return Response(
                {
                    "error": {
                        "type": "Unauthorized",
                        "message": "Authorization Token required.",
                    },
                    "status": 401,
                },
                status=status.HTTP_401_UNAUTHORIZED,
            )

        return wrapper

    return decorator
