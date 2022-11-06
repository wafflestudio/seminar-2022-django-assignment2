from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from blog.views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, \
    CommentUpdateDestroyView

urlpatterns = [
    path('post/', PostListCreateView.as_view()),
    path('post/<int:pid>/', PostRetrieveUpdateDestroyView.as_view()),
    path('comment/<int:pid>/', CommentListCreateView.as_view()),
    path('comment/<int:pid>/<int:cid>', CommentUpdateDestroyView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)