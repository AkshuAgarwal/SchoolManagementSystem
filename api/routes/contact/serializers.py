from rest_framework import serializers

from .models import ContactMessageModel


class ContactMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ContactMessageModel
        exclude = ("id",)
