from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('signup/', UserCreateView.as_view()),
    path('posts/', PostListView.as_view()),
    path('posts/<int:pk>/', PostDetailView.as_view()),
    path('posts/<int:post_pk>/comments/', CommentListView.as_view()),
    path('posts/<int:post_pk>/comments/<int:pk>', CommentUpdateDeleteView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
