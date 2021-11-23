from django.urls import path

from .views import create_user


urlpatterns = [
    path("users/create/", create_user),
]
