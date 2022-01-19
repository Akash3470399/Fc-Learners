from unicodedata import name
from django.urls import path

from . import views

app_name = 'User'

urlpatterns = [
    path('register-or-login/', views.register_or_login, name='register_or_login'),
    path('register/', views.user_register, name="register"),
    path('login/', views.user_login, name="login"),
]
