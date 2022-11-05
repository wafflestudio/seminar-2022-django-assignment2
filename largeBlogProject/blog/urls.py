from rest_framework.routers import DefaultRouter
from django.urls import path, include
from . import views
from rest_registration.api.views import register


urlpatterns = [
    #path('users/', register),
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view())
]
