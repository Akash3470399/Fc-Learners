from unicodedata import name
from django.urls import path

from . import views

app_name = 'User'

urlpatterns = [
    path('register-or-login/', views.register_or_login, name='register_or_login'),
    path('register/', views.user_register_with_email, name="register"),
    path('login/', views.user_login, name="login"),
    path('logout',views.logout_user,name='logout'),
    path('student_dash/', views.student_dash, name="student_dash"),
    path('teacher_dash/', views.teacher_dash, name="teacher_dash"),
    path('dash-blogs-paginated/', views.paginated_blog_list, name="dash_blogs_paginated"),
    path('dash-notes-paginated/', views.paginated_notes_list, name="dash_notes_paginated"),
    path('activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/', views.activate, name='activate'),  
]
