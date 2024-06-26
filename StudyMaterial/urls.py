from django.urls import path
from . import views

app_name = 'StudyMaterial'
urlpatterns = [
    path('', views.index, name = "study_home"),
    path('study-material-listing/',views.study_material_listing,name='study_material_listing'),
    path('add_study_material/',views.add_study_material,name='add_study'),
    path("search-notes/", views.search_notes, name = "search_notes"),
    path('delete-note/<str:pk>/', views.delete_note, name="delete_note"),
    path('update-resource/<str:pk>/', views.ResourceUpdateView.as_view(), name='update_resource'),
    path('delete-resource/<str:pk>/', views.ResourceDeleteView.as_view(), name='delete_resource'),
    path('update-status/', views.change_status, name="change_status"),
]
