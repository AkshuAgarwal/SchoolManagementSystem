from django.apps import apps
from rest_framework import serializers


# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = apps.get_model('root', 'User')
#         exclude = (
#             "last_login",
#             "password",
#             "groups",
#             "user_permissions",
#         )
