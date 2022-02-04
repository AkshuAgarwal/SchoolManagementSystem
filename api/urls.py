from django.urls import path

from .views import contact, user, klass, subject
from .views.klass import all as klass__all
from .views.subject import all as subject__all
from .views.user import me as user__me


urlpatterns = [
    path("contact/", contact.ContactViewSet.as_view(), name="api__contact"),
    path("user/", user.UserViewSet.as_view(), name="api__user"),
    path("user/@me/", user__me.MeViewSet.as_view(), name="api__user__@me"),
    path("class/", klass.ClassViewSet.as_view(), name="api__class"),
    path("class/all/", klass__all.ClassAllViewSet.as_view(), name="api__class__all"),
    path("subject/", subject.SubjectViewSet.as_view(), name="api__subject"),
    path("subject/all/", subject__all.SubjectAllViewSet.as_view(), name="api__subject__all"),
]
