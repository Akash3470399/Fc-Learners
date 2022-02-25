from unicodedata import name
from django.urls import path

from . import views

app_name = 'Blog'

urlpatterns = [
    path('', views.index, name = "blog_home"),
    # path('add-new-post', views.PostCreateView.as_view(), name='add_new_post') ,
    path('add-new-post', views.PostCreateView.as_view(), name='add_new_post') ,
    path('detail-page/<str:pk>/', views.PostDetailView.as_view(), name='blog_detail'),
    path('list/', views.PostListView.as_view(), name="blog_list"),
    path("paginated_post/", views.get_paginated_posts, name="get_paginated_post"),
    path('search/<str:q>/', views.search_blogs, name="blog_search"),
]


