from __future__ import annotations
from typing import TYPE_CHECKING

from rest_framework import serializers

from .models import FileAssets, ImageAssets, Management, Parent, Student, Subject, Teacher, User, Class

if TYPE_CHECKING:
    from rest_framework.request import Request


class FileAssetsSerializer(serializers.Serializer):
    file = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_file(self, obj: FileAssets) -> str:
        request: Request = self.context["request"]
        return request.build_absolute_uri(obj.file.url)

    class Meta:
        model = FileAssets
        fields = ["id", "file", "uploaded_at"]


class ImageAssetsSerializer(serializers.ModelSerializer):
    image = serializers.SerializerMethodField()

    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_image(self, obj: ImageAssets) -> str:
        request: Request = self.context["request"]
        return request.build_absolute_uri(obj.image.url)

    class Meta:
        model = ImageAssets
        fields = ["id", "image", "uploaded_at"]


class UserSerializer(serializers.ModelSerializer):
    avatar = serializers.SerializerMethodField(allow_null=True)

    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def get_avatar(self, obj: User) -> str:
        data = ImageAssetsSerializer(
            instance=obj.avatar, fields={"image"}, context={"request": self.context["request"]}
        ).data
        return data.get("image")

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "first_name",
            "last_name",
            "email_id",
            "avatar",
            "user_type",
            "date_of_birth",
            "gender",
            "contact_no",
            "address",
            "date_joined",
        ]


class ClassSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Class
        fields = [
            "id",
            "grade",
            "section",
        ]


class SubjectSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    class Meta:
        model = Subject
        fields = [
            "id",
            "name",
            "code",
        ]


class ParentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        for field in {"parent"}:
            self.fields[field].context.update(self.context)

    parent = UserSerializer()

    class Meta:
        model = Parent
        fields = [
            "parent",
        ]


class StudentSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        for field in {"student", "parent", "grade"}:
            self.fields[field].context.update(self.context)

    student = UserSerializer()
    parent = ParentSerializer(allow_null=True)
    grade = ClassSerializer(allow_null=True)

    class Meta:
        model = Student
        fields = [
            "id",
            "student",
            "parent",
            "grade",
            "roll_no",
            "year_of_enroll",
            "fee",
        ]


class TeacherSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        for field in {"teacher", "subject", "classes", "owns_class"}:
            self.fields[field].context.update(self.context)

    teacher = UserSerializer()
    subject = SubjectSerializer(allow_null=True)
    classes = ClassSerializer(many=True, allow_null=True)
    owns_class = ClassSerializer(allow_null=True)

    class Meta:
        model = Teacher
        fields = [
            "teacher",
            "subject",
            "year_of_joining",
            "salary",
            "classes",
            "owns_class",
        ]


class ManagementSerializer(serializers.ModelSerializer):
    def __init__(self, *args, **kwargs) -> None:
        fields = kwargs.pop("fields", None)

        super().__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

        for field in {"management"}:
            self.fields[field].context.update(self.context)

    management = UserSerializer()

    class Meta:
        model = Management
        fields = [
            "management",
            "role",
            "year_of_joining",
            "salary",
        ]
