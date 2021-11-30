from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from ..authentication import UserAuthentication


class UnAuthViewSet(APIView):
    authentication_classes = [UserAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        _response = Response()

        _response.delete_cookie("token")
        _response.delete_cookie("csrftoken")

        _response.status_code = status.HTTP_205_RESET_CONTENT

        return _response
