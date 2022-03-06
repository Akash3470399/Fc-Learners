from django.urls import path
from . import views

app_name = 'StudyMaterial'
urlpatterns = [
    path('', views.index, name = "study_home"),
    path('study-material-listing/',views.study_material_listing,name='study_material_listing'),
    path('add_study/',views.add_study_material,name='add_study'),
    path("search-notes/", views.search_notes, name = "search_notes"),
]
