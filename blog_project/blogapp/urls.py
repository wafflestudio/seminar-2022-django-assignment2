from django.urls import path
from .views import PostListCreateView, PostDetailView, CommentListCreateView, CommentDetailView
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:pk>/comments/', CommentListCreateView.as_view()),
    path('posts/<int:pk>/comments/<int:id>/', CommentDetailView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)