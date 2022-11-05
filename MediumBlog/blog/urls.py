from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import PostRetrieveUpdateDestroyView, PostListCreateView, CommentListCreateView, CommentUpdateDestroyView, \
    SignupView, PostCommentRetrieveView, PostListbyTagView, CommentListbyTagView

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>', PostRetrieveUpdateDestroyView.as_view()),
    path('posts/<int:pk>/comments', PostCommentRetrieveView.as_view()),
    path('posts/tags/<str:content>',PostListbyTagView.as_view()),
    path('comments/', CommentListCreateView.as_view()),
    path('comments/<int:pk>', CommentUpdateDestroyView.as_view()),
    path('comments/tags/<str:content>',CommentListbyTagView.as_view()),
    path('register/',SignupView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)