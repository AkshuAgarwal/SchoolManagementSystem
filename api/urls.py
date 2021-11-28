from django.urls import path

from .views import authorize, unauthorize


urlpatterns = [
    path("authorize/", authorize.AuthViewSet.as_view()),
    path("unauthorize/", unauthorize.UnAuthViewSet.as_view()),
]
