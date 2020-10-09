from django.urls import path
from . import views

app_name = "ClanApp"


urlpatterns = [
    path("", views.homepage, name="homepage"),
    path("save/", views.save, name="save"),
    path("delete/", views.delete, name="delete"),
    path("profile/", views.profile, name="profile"),
    path("message/", views.message, name="message"),
    path("message/send", views.send, name="send"),
]