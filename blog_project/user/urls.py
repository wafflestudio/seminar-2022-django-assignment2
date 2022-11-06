from django.urls import path
from .views import RegisterUser, LoginView, FollowUser, UnFollowUser, UserProfile

urlpatterns = [
    path('register/', RegisterUser.as_view()),
    path('login/', LoginView.as_view()),
    path('follow/<int:pk>/', FollowUser.as_view()),
    path('unfollow/<int:pk>/', UnFollowUser.as_view()),
    path('profile/', UserProfile.as_view()),
]
