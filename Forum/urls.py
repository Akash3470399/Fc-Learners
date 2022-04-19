from django import views
from django.urls import path

from . import views

app_name = "Forum"

urlpatterns = [
    path("", views.forum_home, name="forum_home"),
]