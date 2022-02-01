from django.urls import path

from .views import user

urlpatterns = [
    path("user/", user.UserViewSet.as_view(), name="admin__user"),
]
