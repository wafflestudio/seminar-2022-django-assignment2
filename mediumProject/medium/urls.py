from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, CommentUpdateDestroyView, \
    TagToPostView, TagToCommentView

urlpatterns = [
    path('post/', PostListCreateView.as_view()),
    path('post/<int:post_id>/', PostRetrieveUpdateDestroyView.as_view()),
    path('post/<int:post_id>/comment/', CommentListCreateView.as_view()),
    path('post/<int:post_id>/comment/<int:comment_id>', CommentUpdateDestroyView.as_view()),
    path('tag/<str:tag_content>/post', TagToPostView.as_view()),
    path('tag/<str:tag_content>/comment', TagToCommentView.as_view())
]