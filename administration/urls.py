from django.urls import path

from . import views


urlpatterns = [
    path("users/", views.UsersViewSet.as_view(), name="users"),
]
