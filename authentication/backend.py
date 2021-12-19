from __future__ import annotations
from typing import Optional, overload, TYPE_CHECKING

from django.contrib.auth.backends import ModelBackend
from django.utils.translation import gettext_lazy as _

from utils.exceptions import InvalidAuthenticationArguments

from root.models import User as UserModel

if TYPE_CHECKING:
    from django.http.request import HttpRequest


class MyBackend(ModelBackend):
    @overload
    def authenticate(self, request: HttpRequest = ..., username: str = ..., password: str = ...) -> Optional[UserModel]:
        ...

    @overload
    def authenticate(self, request: HttpRequest = ..., email_id: str = ..., password: str = ...) -> Optional[UserModel]:
        ...

    def authenticate(
        self, __r: HttpRequest = None, username: str = None, password: str = None, email_id: str = None
    ) -> Optional[UserModel]:
        if not password:
            raise InvalidAuthenticationArguments("Missing 'password' argument", fields=["password"])

        if username and email_id:
            raise InvalidAuthenticationArguments(
                _("Cannot pass both username and email_id in authenticate()"), fields=["username", "email_id"]
            )

        if username:
            __kwargs = {"username": username}
        elif email_id:
            __kwargs = {"email_id": email_id}
        else:
            raise InvalidAuthenticationArguments(
                _("Missing 'username' or 'email_id' arguments"), fields=["username", "email_id"]
            )

        try:
            user = UserModel.objects.get(**__kwargs)
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if user.check_password(password) and self.user_can_authenticate(user):
                return user

    def get_user(self, user_id: int) -> Optional[UserModel]:
        try:
            user = UserModel.objects.get(id=user_id)
        except UserModel.DoesNotExist:
            return None

        return user if self.user_can_authenticate(user) else None
