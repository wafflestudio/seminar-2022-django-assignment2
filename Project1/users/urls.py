from django.urls import path
from .views import UserListCreateView, UserFollowingView, UserFollowersView, UserProfilePhotoView, UserPostListView, UserRetrieveUpdateDestroyView

urlpatterns = [
    path('users/', UserListCreateView.as_view()),
    path('@<slug:username>/following/', UserFollowingView.as_view()),
    path('@<slug:username>/followers/', UserFollowersView.as_view()),
    path('@<slug:username>/profile_photo', UserProfilePhotoView.as_view()),
    path('@<slug:username>/posts', UserPostListView),
    path('@<slug:username>/profile', UserRetrieveUpdateDestroyView),
]