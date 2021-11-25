import uuid
import hashlib

from django.apps import apps
from django.db import models
from django.contrib.auth.base_user import BaseUserManager as _BUM
from django.utils import timezone
from django.utils.translation import ugettext_lazy as _


class UserManager(_BUM):
    def create_user(
        self,
        username,
        first_name,
        last_name,
        email_id,
        user_type,
        date_of_birth,
        contact_no,
        address,
        password,
        **extra_fields,
    ):
        FIELDS = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email_id": email_id,
            "user_type": user_type,
            "date_of_birth": date_of_birth,
            "contact_no": contact_no,
            "address": address,
            "password": password,
        }
        for key, value in FIELDS.items():
            if isinstance(value, list):
                FIELDS[key] = value[0]

        if FIELDS["user_type"] not in {"s", "t", "p", "m"}:
            raise ValueError(_('User Type for normal users can only be "s, t, p, or m"'))

        if not all({FIELDS.values()}):
            raise ValueError(_("All the fields must be set. For Optional fields, pass an empty string as the value."))

        email_id = self.normalize_email(FIELDS["email_id"])

        date_of_birth = FIELDS["date_of_birth"]

        extra_fields["is_staff"] = False
        extra_fields["is_superuser"] = False
        extra_fields["is_active"] = True

        cur_time = timezone.now()

        user = self.model(
            creation_time=cur_time,
            **FIELDS,
            **extra_fields,
        )
        user.set_password(FIELDS["password"])
        user.save()

        auth = apps.get_model("administration", "AuthorizationModel").objects.create(user)

        return user

    def create_superuser(
        self,
        username,
        first_name,
        last_name,
        email_id,
        date_of_birth,
        contact_no,
        address,
        password,
        **extra_fields,
    ):
        FIELDS = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email_id": email_id,
            "user_type": "a",
            "date_of_birth": date_of_birth,
            "contact_no": contact_no,
            "address": address,
            "password": password,
        }
        for key, value in FIELDS.items():
            if isinstance(value, list):
                FIELDS[key] = value[0]

        if not all({FIELDS.values()}):
            raise ValueError(_("All the fields must be set. For Optional fields, pass an empty string as the value."))

        email_id = self.normalize_email(FIELDS["email_id"])

        date_of_birth = FIELDS["date_of_birth"]

        extra_fields["is_staff"] = True
        extra_fields["is_superuser"] = True
        extra_fields["is_active"] = True

        cur_time = timezone.now()

        user = self.model(
            creation_time=cur_time,
            **FIELDS,
            **extra_fields,
        )
        user.set_password(FIELDS["password"])
        user.save()

        auth = apps.get_model("administration", "AuthorizationModel").objects.create(user)

        return user


class AuthorizationManager(models.Manager):
    def create(self, user):
        auth_token = (
            f"{hashlib.md5(str(user.id).encode('ascii')).hexdigest()}."
            f"{hashlib.sha256(user.creation_time.isoformat().encode('ascii')).hexdigest()}."
            f"{uuid.uuid4()}"
        )
        auth = self.model(
            user=user,
            authorization_token=auth_token,
        )
        auth.save()
        return auth
