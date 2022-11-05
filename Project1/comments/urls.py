from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentListCreateView, CommentUpdateDestroyView, CommentListByTagView

urlpatterns = [
    path('list/', CommentListCreateView.as_view()),
    path('<int:comment_id>/', CommentUpdateDestroyView.as_view()),
    path('tag/<str:content>', CommentListByTagView.as_view(), name='comments-by-tag')
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
