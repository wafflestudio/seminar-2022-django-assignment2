from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import CommentListCreateView, CommentUpdateDestroyView

urlpatterns = [
    path('list/', CommentListCreateView.as_view()),
    path('<int:comment_id>/', CommentUpdateDestroyView.as_view()),
]

# urlpatterns = format_suffix_patterns(urlpatterns, allowed=['json', 'html'])
