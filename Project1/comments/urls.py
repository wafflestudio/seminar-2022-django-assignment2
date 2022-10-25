from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentListView, CommentCreateView, CommentUpdateDestoryView

urlpatterns = [
    path('comments/list', CommentListView.as_view()),
    path('comments/<int:pk>', CommentUpdateDestoryView),
]

urlpatterns = format_suffix_patterns(urlpatterns)
