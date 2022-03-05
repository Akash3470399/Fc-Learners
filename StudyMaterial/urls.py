from django.urls import path
from . import views

app_name = 'StudyMaterial'
urlpatterns = [
    path('', views.index, name = "study_home"),
    path('study_listing',views.study_listing,name='study_listing'),
    path('add_study',views.add_study,name='add_study'),
    path('logout',views.Logout,name='logout'),
    path("paginated_material/", views.get_paginated_material, name="get_paginated_material"),
    #path('search/<str:q>/', views.search_study, name="study_search"),
]
