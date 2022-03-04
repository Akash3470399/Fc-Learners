from unicodedata import name
from django.urls import path

from . import views

app_name = 'User'

urlpatterns = [
    path('register-or-login/', views.register_or_login, name='register_or_login'),
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
    path('student_dash/', views.student_dash, name="student_dash"),
    path('teacher_dash/', views.teacher_dash, name="teacher_dash"),
]
