from datetime import datetime
from dateutil import parser as dateparser

from django.apps import apps
from django.db.models import Q as OR
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.base_user import BaseUserManager as _BUM
from django.utils.translation import gettext_lazy as _

from utils.exceptions import AlreadyExists, MissingRequiredFields
from utils.files import parse_data_scheme


class UserManager(_BUM):
    REQUIRED_FIELDS = [
        "username",
        "first_name",
        "email_id",
        "user_type",
        "date_of_birth",
        "gender",
        "contact_no",
        "password",
    ]

    def create_user(
        self,
        username,
        first_name,
        last_name,
        email_id,
        avatar,
        user_type,
        date_of_birth,
        gender,
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
            "avatar": avatar,
            "user_type": user_type,
            "date_of_birth": date_of_birth,
            "gender": gender,
            "contact_no": contact_no,
            "address": address,
            "password": password,
        }

        # Filtering
        for key, value in FIELDS.items():
            if isinstance(value, list):
                FIELDS[key] = value[0]

        for key, value in FIELDS.items():
            if not value:
                FIELDS.pop(key)

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        # Formatting
        FIELDS["email_id"] = self.normalize_email(FIELDS["email_id"])

        try:
            FIELDS["date_of_birth"] = dateparser.parse(FIELDS["date_of_birth"]).date()
        except dateparser.ParserError:
            raise ValidationError(message=_("Invalid Date format for date_of_birth"), code="invalid")

        # Format/Value validity checking
        if not all(ord(char) < 128 for char in FIELDS["password"]):
            raise ValidationError(message=_("password should only contain ASCII characters"), code="invalid")

        if not all(ord(char) < 128 for char in FIELDS["username"]):
            raise ValidationError(message=_("username should only contain ASCII characters"), code="invalid")

        if FIELDS["user_type"] not in {"s", "t", "p", "m"}:
            raise ValidationError(message=_('user_type for non-admin users can only be "s, t, p, m"'), code="invalid")

        if FIELDS["gender"] not in {"m", "f", "o"}:
            raise ValidationError(message=_('gender can only be one of "m, f, o"'), code="invalid")

        EmailValidator(message=_("Invalid email_id"))(FIELDS["email_id"])

        RegexValidator(
            regex=r"^\+[0-9]{5,14}$",
            message=_(
                "Invalid contact_no. Contact No. must be entered in the format: '+999999999999' (with country code). Up to 15 digits allowed."
            ),
        )(FIELDS["contact_no"])

        # Unique constraint checking
        existing_fields: set = {}
        __existing_user = self.filter(OR(username=FIELDS["username"]) | OR(email_id=FIELDS["email_id"]))
        if __existing_user:
            for __user in __existing_user:
                if __user["username"] == FIELDS["username"]:
                    existing_fields.add("username")
                if __user["email_id"] == FIELDS["email_id"]:
                    existing_fields.add("email_id")

                if {"username", "email_id"} == existing_fields:
                    break

            raise AlreadyExists(existing_fields=list(existing_fields))

        # Creating Avatar
        if pfp_scheme := FIELDS["avatar"]:
            __parsed = parse_data_scheme(pfp_scheme)

            if __parsed["media_type"] != "image":
                raise ValidationError("Invalid avatar data URI")

            if x := __parsed["media_format"] not in {"jpg", "jpeg", "png", "gif"}:
                raise ValidationError(f"Image format {x!r} is invalid or not supported")

            _image = ImageFile(
                file=__parsed["decoded_media_data"],
                name=f"avatar_{FIELDS['username']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{__parsed['media_format']}",
            )

            asset = apps.get_model("root.ImageAssets").objects.create(image=_image)
            FIELDS["avatar"] = int(asset.id)

        FIELDS["is_staff"] = FIELDS["user_type"] == "m"
        FIELDS["is_superuser"] = False
        FIELDS["is_active"] = True

        password = FIELDS.pop("password")
        user = self.model(**FIELDS, **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(
        self,
        username,
        first_name,
        last_name,
        email_id,
        avatar,
        date_of_birth,
        gender,
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
            "avatar": avatar,
            "use_type": "a",
            "date_of_birth": date_of_birth,
            "gender": gender,
            "contact_no": contact_no,
            "address": address,
            "password": password,
        }

        # Filtering
        for key, value in FIELDS.items():
            if isinstance(value, list):
                FIELDS[key] = value[0]

        for key, value in FIELDS.items():
            if not value:
                FIELDS.pop(key)

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        # Formatting
        FIELDS["email_id"] = self.normalize_email(FIELDS["email_id"])

        try:
            FIELDS["date_of_birth"] = dateparser.parse(FIELDS["date_of_birth"]).date()
        except dateparser.ParserError:
            raise ValidationError(message=_("Invalid Date format for date_of_birth"), code="invalid")

        # Format/Value validity checking
        if not all(ord(char) < 128 for char in FIELDS["password"]):
            raise ValidationError(message=_("password should only contain ASCII characters"), code="invalid")

        if not all(ord(char) < 128 for char in FIELDS["username"]):
            raise ValidationError(message=_("username should only contain ASCII characters"), code="invalid")

        if FIELDS["gender"] not in {"m", "f", "o"}:
            raise ValidationError(message=_('gender can only be one of "m, f, o"'), code="invalid")

        EmailValidator(message=_("Invalid email_id"))(FIELDS["email_id"])

        RegexValidator(
            regex=r"^\+[0-9]{5,14}$",
            message=_(
                "Invalid contact_no. Contact No. must be entered in the format: '+999999999999' (with country code). Up to 15 digits allowed."
            ),
        )(FIELDS["contact_no"])

        # Unique constraint checking
        existing_fields: set = {}
        __existing_user = self.filter(OR(username=FIELDS["username"]) | OR(email_id=FIELDS["email_id"]))
        if __existing_user:
            for __user in __existing_user:
                if __user["username"] == FIELDS["username"]:
                    existing_fields.add("username")
                if __user["email_id"] == FIELDS["email_id"]:
                    existing_fields.add("email_id")

                if {"username", "email_id"} == existing_fields:
                    break

            raise AlreadyExists(existing_fields=list(existing_fields))

        # Creating Avatar
        if pfp_scheme := FIELDS["avatar"]:
            __parsed = parse_data_scheme(pfp_scheme)

            if __parsed["media_type"] != "image":
                raise ValidationError("Invalid avatar data URI")

            if x := __parsed["media_format"] not in {"jpg", "jpeg", "png", "gif"}:
                raise ValidationError(f"Image format {x!r} is invalid or not supported")

            _image = ImageFile(
                file=__parsed["decoded_media_data"],
                name=f"avatar_{FIELDS['username']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{__parsed['media_format']}",
            )

            asset = apps.get_model("root.ImageAssets").objects.create(image=_image)
            FIELDS["avatar"] = int(asset.id)

        FIELDS["is_staff"] = True
        FIELDS["is_superuser"] = True
        FIELDS["is_active"] = True

        password = FIELDS.pop("password")
        user = self.model(**FIELDS, **extra_fields)
        user.set_password(password)
        user.save()

        return user
