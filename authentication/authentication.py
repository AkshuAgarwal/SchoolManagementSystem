from __future__ import annotations
from typing import Optional, TYPE_CHECKING, Tuple

from django.conf import settings
from django.utils.translation import gettext_lazy as _

from rest_framework.authentication import CSRFCheck
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.settings import api_settings as simplejwt_settings

if TYPE_CHECKING:
    from django.http.request import HttpRequest
    from rest_framework_simplejwt.tokens import AccessToken

    from root.models import User as UserModel


def enforce_csrf(request: HttpRequest) -> None:
    check = CSRFCheck()
    check.process_request(request)

    reason = check.process_view(request, None, (), {})
    if reason:
        raise PermissionDenied(_("CSRF Failed: %(reason)s") % {"reason": reason})


class CSRFExemptAuthentication(JWTAuthentication):
    def authenticate(self, request: HttpRequest) -> Tuple[Optional[UserModel], AccessToken]:
        header = self.get_header(request)

        if header is None:
            raw_token = request.COOKIES.get(settings.SIMPLE_JWT["AUTH_COOKIE"]) or None
        else:
            raw_token = self.get_raw_token(header)

        if raw_token is None:
            return None

        validated_token = self.get_validated_token(raw_token)
        if not validated_token:
            return None
        return self.get_user(validated_token), validated_token

    def get_validated_token(self, raw_token):
        for AuthToken in simplejwt_settings.AUTH_TOKEN_CLASSES:
            try:
                return AuthToken(raw_token)
            except TokenError as e:
                pass

        return None


class Authentication(CSRFExemptAuthentication):
    def authenticate(self, request: HttpRequest) -> Tuple[Optional[UserModel], AccessToken]:
        enforce_csrf(request)
        return super().authenticate(request)
