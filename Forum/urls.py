from django import views
from django.urls import path

from . import views

app_name = "Forum"

urlpatterns = [
    path("", views.forum_home, name="forum_home"),
    path("get-question/<str:pk>/", views.get_question, name="get_question"),
    path("add-question/", views.add_question, name="add_question"),
    path("add-answer/<str:pk>/", views.add_answer, name="add_answer"),
]