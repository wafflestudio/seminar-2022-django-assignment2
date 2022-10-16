from django.urls import path
from .views import PostList, PostDetail, CommentList, TagPostList, TagCommentList, UserCreate, LoginView, CommentDetail, ProfileView, NotificationList, ClapseList

urlpatterns = [
    path('auth/register/', UserCreate.as_view()),
    path('auth/login/', LoginView.as_view()),
    path('user/profile/', ProfileView.as_view()),
    path('user/notification/', NotificationList.as_view()),
    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/<int:pk>/clapse/', ClapseList.as_view()),
    path('post/<int:pk>/comment/', CommentList.as_view()),
    path('post/<int:pk>/comment/<int:pk2>', CommentDetail.as_view()),
    path('tag/post/', TagPostList.as_view()),
    path('tag/comment/', TagCommentList.as_view())
]
