from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pid>/', PostDetailView.as_view()),
    path('posts/<int:pid>/comments/', CommentView.as_view()),
    path('comments/<int:cid>/', CommentDetailView.as_view()),
    path('tags/', TagListViewOnly.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
