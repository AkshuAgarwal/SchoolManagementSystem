from django.urls import path

from .views import contact


urlpatterns = [
    path('contact/', contact.ContactViewSet.as_view(), name="contact"),
]
