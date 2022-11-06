from django.urls import path

from . import views

urlpatterns = [
    path('posts/', views.PostList.as_view()),
    path('posts/<int:pk>/', views.PostDetail.as_view()),
    path('comments/', views.CommentList.as_view()),
    path('comments/<int:pk>/', views.CommentDetail.as_view()),
    path('users/<int:pk>/following/', views.UserFollowingList.as_view()),
    path('users/<int:pk>/following/<int:other_pk>/', views.UserFollowingDestroy.as_view()),
    path('users/<int:pk>/followers/', views.UserFollowersList.as_view())
]
