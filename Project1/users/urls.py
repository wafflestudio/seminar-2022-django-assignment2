from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import UserListView, UserCreateView, UserFollowingView, \
    UserFollowersView, UserPostListView, UserProfileView, UserFollowView, \
    UserUnfollowView, UserCommentListView

urlpatterns = [
    path('list/', UserListView.as_view()),
    path('signup/', UserCreateView.as_view()),
    path('@<slug:username>/following/', UserFollowingView.as_view(), name='following-list'),
    path('@<slug:username>/followers/', UserFollowersView.as_view(), name='followers-list'),
    path('@<slug:username>/posts_of_user', UserPostListView.as_view()),
    path('@<slug:username>/comments_of_user', UserCommentListView.as_view()),
    path('@<slug:username>/', UserProfileView.as_view(), name='user-detail'),
    path('follow/@<slug:following_user_name>', UserFollowView.as_view()),
    path('unfollow/@<slug:following_user_name>', UserUnfollowView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])