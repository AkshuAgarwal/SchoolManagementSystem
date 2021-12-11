from django.urls import path

from .routes import contact, timetable


urlpatterns = [
    path("contact/", contact.ContactMessagesView.as_view()),
    path("timetable/", timetable.TimeTableView.as_view()),
]
