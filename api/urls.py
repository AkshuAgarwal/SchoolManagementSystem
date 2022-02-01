from django.urls import path

from .views import contact, user
from .views.user import me


urlpatterns = [
    path("contact/", contact.ContactViewSet.as_view(), name="api__contact"),
    path("user/", user.UserViewSet.as_view(), name="api__user"),
    path("user/@me/", me.MeViewSet.as_view(), name="apu__user__@me"),
]
