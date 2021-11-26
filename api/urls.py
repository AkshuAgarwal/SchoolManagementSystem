from django.urls import path

from . import views


urlpatterns = [
    path("authorize/", views.AuthViewSet.as_view()),
]
