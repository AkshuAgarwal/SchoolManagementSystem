from django.urls import path

from .routes import contact

urlpatterns = [
    path("contact/", contact.ContactMessagesView.as_view()),
]
