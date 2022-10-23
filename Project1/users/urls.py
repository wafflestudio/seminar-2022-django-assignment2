from django.urls import path
from .views import UserListCreateView, UserFollowingView, UserFollowersView

urlpatterns = [
    path('makeuser/', UserListCreateView.as_view()),
    path('@<slug:username>/following/', UserFollowingView.as_view()),
    path('@<slug:username>/followers/', UserFollowersView.as_view()),
]