from django.urls import path

from .views import authenticate, unauthenticate, refresh_token, reset_password


urlpatterns = [
    path("authenticate/", authenticate.AuthViewSet.as_view(), name="authenticate"),
    path("unauthenticate/", unauthenticate.UnAuthViewSet.as_view(), name="unauthenticate"),
    path("token/refresh/", refresh_token.RefreshTokenViewSet.as_view(), name="refresh_token"),
    path("password/reset/", reset_password.ResetPasswordViewSet.as_view(), name="reset_password"),
]
