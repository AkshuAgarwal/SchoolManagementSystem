from django.urls import path

from .views import authenticate, unauthenticate, refresh_token


urlpatterns = [
    path("authenticate/", authenticate.AuthViewSet.as_view(), name="authenticate"),
    path("unauthenticate/", unauthenticate.UnAuthViewSet.as_view(), name="unauthenticate"),
    path("token/refresh/", refresh_token.RefreshTokenViewSet.as_view(), name="refresh_token"),
]
