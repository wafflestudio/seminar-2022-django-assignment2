from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, CommentUpdateDestroyView

urlpatterns = [
    path('post/', PostListCreateView.as_view()),
    path('post/<int:post_id>/', PostRetrieveUpdateDestroyView.as_view()),
    path('post/<int:post_id>/comment/', CommentListCreateView.as_view()),
    path('post/<int:post_id>/comment/<int:comment_id>', CommentUpdateDestroyView.as_view()),
]