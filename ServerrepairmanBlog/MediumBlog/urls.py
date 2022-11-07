from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from MediumBlog.views import *

urlpatterns = [
    path('posts/', PostPermissionListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('posts/tags/<str:tag>/', PostPermissionListCreateViewByTag.as_view()),
    path('posts/tags/', PostTagListView.as_view()),
    path('comments/tags/', CommentTagListView.as_view()),
    path('comments/', CommentPermissionListCreateView.as_view()),
    path('comments/<int:pk>/', CommentRetrieveUpdateDestroyView.as_view()),
    path('posts/<int:post_id>/comments/', CommentPermissionListCreateViewByPost.as_view()),
    path('register/', SignupView.as_view()),
    path('login/', SigninView().as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
