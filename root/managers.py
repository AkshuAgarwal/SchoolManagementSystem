from __future__ import annotations
from typing import Any, List, Literal, Optional, Union, TYPE_CHECKING, overload

from datetime import datetime
from dateutil import parser as dateparser

from django.apps import apps
from django.db import models
from django.db.models import Q as OR
from django.core.files.images import ImageFile
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator, EmailValidator
from django.contrib.auth.base_user import BaseUserManager as _BUM
from django.contrib.auth.password_validation import validate_password

from utils.py.exceptions import AlreadyExists, MissingRequiredFields
from utils.py.files import parse_data_scheme

if TYPE_CHECKING:
    from .models import (
        User as UserModel,
        Student as StudentModel,
        Teacher as TeacherModel,
        Parent as ParentModel,
        Management as ManagementModel,
        Class as ClassModel,
        Subject as SubjectModel,
    )


class StudentManager(models.Manager):
    REQUIRED_FIELDS = ["student", "roll_no", "year_of_enroll", "fee"]

    def create(
        self,
        *,
        student: Union[int, UserModel],
        parent: Optional[Union[int, UserModel]] = None,
        grade: Optional[Union[int, ClassModel]] = None,
        roll_no: int,
        year_of_enroll: int,
        fee: int,
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> StudentModel:
        FIELDS = {
            "student": student,
            "parent": parent,
            "grade": grade,
            "roll_no": roll_no,
            "year_of_enroll": year_of_enroll,
            "fee": fee,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        if isinstance(FIELDS["student"], int):
            FIELDS["student_id"] = FIELDS.pop("student")
        if isinstance(FIELDS["parent"], int):
            FIELDS["parent_id"] = FIELDS.pop("parent")
        if isinstance(FIELDS["grade"], int):
            FIELDS["grade_id"] = FIELDS.pop("grade")

        if user := FIELDS.get("student"):
            _existing_users = self.filter(student=user)
        elif user_id := FIELDS.get("student_id"):
            _existing_users = self.filter(student__id=user_id)
        if _existing_users:
            raise AlreadyExists(colliding_fields=["student"])

        if not 1000 < FIELDS["year_of_enroll"] <= datetime.now().year:
            raise ValidationError("Invalid year_of_enroll")

        student: StudentModel = self.model(**FIELDS, **extra_fields)
        if not nosave:
            student.save()

        return student


class TeacherManager(models.Manager):
    REQUIRED_FIELDS = ["teacher", "year_of_joining", "salary"]

    @overload
    def create(
        self,
        *,
        teacher: Union[int, UserModel],
        subject: Optional[Union[int, SubjectModel]] = ...,
        year_of_joining: int,
        salary: int,
        classes: Optional[List[Union[int, ClassModel]]] = ...,
        owns_class: Optional[Union[int, ClassModel]] = ...,
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> TeacherModel:
        ...

    @overload
    def create(
        self,
        *,
        teacher: Union[int, UserModel],
        subject: Optional[Union[int, SubjectModel]] = ...,
        year_of_joining: int,
        salary: int,
        owns_class: Optional[Union[int, ClassModel]] = ...,
        nosave: Optional[bool] = True,
        **extra_fields: Any,
    ) -> TeacherModel:
        ...

    def create(
        self,
        *,
        teacher: Union[int, UserModel],
        subject: Optional[Union[int, SubjectModel]] = None,
        year_of_joining: int,
        salary: int,
        classes: Optional[List[Union[int, ClassModel]]] = None,
        owns_class: Optional[Union[int, ClassModel]] = None,
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> TeacherModel:
        FIELDS = {
            "teacher": teacher,
            "subject": subject,
            "year_of_joining": year_of_joining,
            "salary": salary,
            "owns_class": owns_class,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        if isinstance(FIELDS["teacher"], int):
            FIELDS["teacher_id"] = FIELDS.pop("teacher")
        if isinstance(FIELDS["owns_class"], int):
            FIELDS["owns_class_id"] = FIELDS.pop("owns_class")

        if user := FIELDS.get("teacher"):
            _existing_users = self.filter(teacher=user)
        elif user_id := FIELDS.get("student_id"):
            _existing_users = self.filter(teacher__id=user_id)
        if _existing_users:
            raise AlreadyExists(colliding_fields=["teacher"])

        if not 1000 < FIELDS["year_of_joining"] <= datetime.now().year:
            raise ValidationError("Invalid year_of_joining")

        teacher: TeacherModel = self.model(**FIELDS, **extra_fields)
        if not nosave:
            teacher.save()

            # classes can't be added to unsaved teacher, therefore this should be done manually if nosave=True.
            if classes and isinstance(classes, list):
                teacher.classes.add(*classes)

        return teacher


class ParentManager(models.Manager):
    REQUIRED_FIELDS = ["parent"]

    def create(
        self,
        *,
        parent: Union[int, UserModel],
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> ParentModel:
        FIELDS = {
            "parent": parent,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        if isinstance(FIELDS["parent"], int):
            FIELDS["parent_id"] = FIELDS.pop("parent")

        if user := FIELDS.get("parent"):
            _existing_users = self.filter(parent=user)
        elif user_id := FIELDS.get("parent_id"):
            _existing_users = self.filter(parent__id=user_id)
        if _existing_users:
            raise AlreadyExists(colliding_fields=["parent"])

        parent: ParentModel = self.model(**FIELDS, **extra_fields)
        if not nosave:
            parent.save()

        return parent


class ManagementManager(models.Manager):
    REQUIRED_FIELDS = ["management", "year_of_joining", "salary"]

    def create(
        self,
        *,
        management: Union[int, UserModel],
        year_of_joining: int,
        salary: int,
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> TeacherModel:
        FIELDS = {
            "management": management,
            "year_of_joining": year_of_joining,
            "salary": salary,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        if isinstance(FIELDS["management"], int):
            FIELDS["management_id"] = FIELDS.pop("management")

        if user := FIELDS.get("management"):
            _existing_users = self.filter(management=user)
        elif user_id := FIELDS.get("management_id"):
            _existing_users = self.filter(management__id=user_id)
        if _existing_users:
            raise AlreadyExists(colliding_fields=["management"])

        if not 1000 < FIELDS["year_of_joining"] <= datetime.now().year:
            raise ValidationError("Invalid year_of_joining")

        management: ManagementModel = self.model(**FIELDS, **extra_fields)
        if not nosave:
            management.save()

        return management


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

    @overload
    def create(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = ...,
        email_id: str,
        avatar: Optional[str] = ...,
        user_type: Literal["s"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = ...,
        password: str,
        parent: Optional[Union[int, UserModel]] = ...,
        grade: Optional[Union[int, ClassModel]] = ...,
        roll_no: int,
        year_of_enroll: int,
        fee: int,
    ) -> StudentModel:
        ...

    @overload
    def create(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = ...,
        email_id: str,
        avatar: Optional[str] = ...,
        user_type: Literal["t"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = ...,
        password: str,
        subject: Optional[Union[int, SubjectModel]] = ...,
        year_of_joining: int,
        salary: int,
        classes: Optional[List[Union[int, ClassModel]]] = ...,
        owns_class: Optional[Union[int, ClassModel]] = ...,
    ) -> TeacherModel:
        ...

    @overload
    def create(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = ...,
        email_id: str,
        avatar: Optional[str] = ...,
        user_type: Literal["p"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = ...,
        password: str,
    ) -> ParentModel:
        ...

    @overload
    def create(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = ...,
        email_id: str,
        avatar: Optional[str] = ...,
        user_type: Literal["m"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = ...,
        password: str,
        year_of_joining: int,
        salary: int,
    ) -> ManagementModel:
        ...

    def create(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = None,
        email_id: str,
        avatar: Optional[str] = None,
        user_type: Literal["s", "p", "t", "m"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = None,
        password: str,
        parent: Optional[Union[int, UserModel]] = None,
        grade: Optional[Union[int, ClassModel]] = None,
        roll_no: Optional[int] = None,
        year_of_enroll: Optional[int] = None,
        fee: Optional[int] = None,
        subject: Optional[Union[int, SubjectModel]] = None,
        classes: Optional[List[Union[int, ClassModel]]] = None,
        owns_class: Optional[Union[int, ClassModel]] = None,
        year_of_joining: Optional[int] = None,
        salary: Optional[int] = None,
    ) -> Union[StudentModel, TeacherModel, ParentModel, ManagementModel]:
        USER_FIELDS = {
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
        raw_user = self.create_user(**USER_FIELDS, nosave=True)

        if user_type == "s":
            USERTYPE_FIELDS = {
                "parent": parent,
                "grade": grade,
                "roll_no": roll_no,
                "year_of_enroll": year_of_enroll,
                "fee": fee,
            }
            user = apps.get_model("root.Student").objects.create(student=raw_user, **USERTYPE_FIELDS, nosave=True)
        elif user_type == "t":
            USERTYPE_FIELDS = {
                "subject": subject,
                "year_of_joining": year_of_joining,
                "salary": salary,
                "owns_class": owns_class,
            }
            user = apps.get_model("root.Teacher").objects.create(teacher=raw_user, **USERTYPE_FIELDS, nosave=True)
        elif user_type == "p":
            USERTYPE_FIELDS = {}
            user = apps.get_model("root.Parent").objects.create(parent=raw_user, **USERTYPE_FIELDS, nosave=True)
        elif user_type == "m":
            USERTYPE_FIELDS = {
                "salary": salary,
                "year_of_joining": year_of_joining,
            }
            user = apps.get_model("root.Management").objects.create(management=raw_user, **USERTYPE_FIELDS, nosave=True)

        # If we reached here, it means all validations are passed and we can safely save the user
        raw_user.save()
        user.save()

        # Also add the classes to saved teacher object which got skipped due to nosave=True
        if user_type == "t":
            user.classes.add(*classes)

        return user

    def create_user(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = None,
        email_id: str,
        avatar: Optional[str] = None,
        user_type: Literal["s", "p", "t", "m"],
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = None,
        password: str,
        nosave: Optional[bool] = False,
        **extra_fields: Any,
    ) -> UserModel:
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

        for key, value in FIELDS.copy().items():
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
        colliding_fields: set = set()
        _existing_users = self.filter(OR(username=FIELDS["username"]) | OR(email_id=FIELDS["email_id"]))
        if _existing_users:
            for __user in _existing_users:
                if __user.username == FIELDS["username"]:
                    colliding_fields.add("username")
                if __user.email_id == FIELDS["email_id"]:
                    colliding_fields.add("email_id")

                if {"username", "email_id"} == colliding_fields:
                    break

            raise AlreadyExists(colliding_fields=list(colliding_fields))

        # Creating Avatar
        if pfp_scheme := FIELDS.get("avatar"):
            __parsed = parse_data_scheme(pfp_scheme)

            if __parsed["type"] != "image":
                raise ValidationError("Invalid avatar data URI")

            if x := __parsed["format"] not in {"jpg", "jpeg", "png", "gif"}:
                raise ValidationError(f"Image format {x!r} is invalid or not supported")

            _image = ImageFile(
                file=__parsed["file_like"],
                name=f"avatar_{FIELDS['username']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{__parsed['format']}",
            )

            asset = apps.get_model("root.ImageAssets").objects.create(image=_image)
            FIELDS["avatar"] = asset

        FIELDS["is_staff"] = FIELDS["user_type"] == "m"
        FIELDS["is_superuser"] = False
        FIELDS["is_active"] = True

        password = FIELDS.pop("password")
        user: UserModel = self.model(**FIELDS, **extra_fields)
        validate_password(password, user)
        user.set_password(password)

        if not nosave:
            user.save()

        return user

    def create_superuser(
        self,
        *,
        username: str,
        first_name: str,
        last_name: Optional[str] = None,
        email_id: str,
        avatar: Optional[str] = None,
        date_of_birth: str,
        gender: Literal["m", "f", "o"],
        contact_no: str,
        address: Optional[str] = None,
        password: str,
        **extra_fields: Any,
    ) -> UserModel:
        FIELDS = {
            "username": username,
            "first_name": first_name,
            "last_name": last_name,
            "email_id": email_id,
            "avatar": avatar,
            "user_type": "a",
            "date_of_birth": date_of_birth,
            "gender": gender,
            "contact_no": contact_no,
            "address": address,
            "password": password,
        }

        for key, value in FIELDS.copy().items():
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
        colliding_fields: set = set()
        _existing_users = self.filter(OR(username=FIELDS["username"]) | OR(email_id=FIELDS["email_id"]))
        if _existing_users:
            for __user in _existing_users:
                if __user.username == FIELDS["username"]:
                    colliding_fields.add("username")
                if __user.email_id == FIELDS["email_id"]:
                    colliding_fields.add("email_id")

                if {"username", "email_id"} == colliding_fields:
                    break

            raise AlreadyExists(colliding_fields=list(colliding_fields))

        # Creating Avatar
        if pfp_scheme := FIELDS.get("avatar"):
            __parsed = parse_data_scheme(pfp_scheme)

            if __parsed["type"] != "image":
                raise ValidationError("Invalid avatar data URI")

            if x := __parsed["format"] not in {"jpg", "jpeg", "png", "gif"}:
                raise ValidationError(f"Image format {x!r} is invalid or not supported")

            _image = ImageFile(
                file=__parsed["file_like"],
                name=f"avatar_{FIELDS['username']}_{datetime.now().strftime('%Y%m%d%H%M%S')}.{__parsed['format']}",
            )

            asset = apps.get_model("root.ImageAssets").objects.create(image=_image)
            FIELDS["avatar"] = asset

        FIELDS["is_staff"] = True
        FIELDS["is_superuser"] = True
        FIELDS["is_active"] = True

        password = FIELDS.pop("password")
        user: UserModel = self.model(**FIELDS, **extra_fields)
        validate_password(password, user)
        user.set_password(password)
        user.save()

        return user


class ClassManager(models.Manager):
    REQUIRED_FIELDS = ["grade"]

    def create(
        self,
        *,
        grade: str,
        section: Optional[str] = None,
        **extra_fields: Any,
    ) -> ClassModel:
        FIELDS = {
            "grade": grade,
            "section": section,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        _existing_classes = self.filter(**FIELDS)
        if _existing_classes:
            raise AlreadyExists()

        klass: ClassModel = self.model(**FIELDS, **extra_fields)
        klass.save()

        return klass


class SubjectManager(models.Manager):
    REQUIRED_FIELDS = ["name", "code"]

    def create(
        self,
        *,
        name: str,
        code: int,
        **extra_fields: Any,
    ) -> SubjectModel:
        FIELDS = {
            "name": name,
            "code": code,
        }

        missing_fields = []
        for required_field in self.REQUIRED_FIELDS:
            if not FIELDS.get(required_field):
                missing_fields.append(required_field)
        if missing_fields:
            raise MissingRequiredFields(missing_fields=missing_fields)

        _existing_subjects = self.filter(**FIELDS)
        if _existing_subjects:
            raise AlreadyExists()

        subject: SubjectModel = self.model(**FIELDS, **extra_fields)
        subject.save()

        return subject
