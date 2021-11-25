from rest_framework import authentication
from rest_framework.exceptions import AuthenticationFailed

from .models import AuthorizationModel


class UserAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        auth_token = request.headers.get("X-Authorization-Token")
        if auth_token is not None:
            try:
                if len(splitted := auth_token.split(" ")) == 2:
                    keyword, token = splitted

                    if keyword == "Bearer":
                        auth = AuthorizationModel.objects.get(authorization_token=token)
                        return auth.user, auth

                    raise AuthenticationFailed("Invalid token type passed", 401)

                raise AuthenticationFailed("Invalid Authorization token", 401)

            except AuthorizationModel.DoesNotExist:
                return AuthenticationFailed("Invalid Authorization token", 401)

        return AuthenticationFailed("Authorization token required", 401)
