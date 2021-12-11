from rest_framework import serializers

from .models import TimetableModel


class TimetableSerializer(serializers.ModelSerializer):
    class Meta:
        model = TimetableModel
        exclude = ("id",)
