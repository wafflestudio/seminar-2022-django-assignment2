from django.urls import path
from blog.views import PostListCreateView, PostRetrieveUpdateDestroyView, \
    CommentRetrieveUpdateDestroyView, CommentListCreateView, TaggedPostListView, TaggedCommentListView

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('posts/<int:pk>/comments/<int:id>/', CommentRetrieveUpdateDestroyView.as_view()),
    path('posts/<int:pk>/comments/', CommentListCreateView.as_view()),
    path('tag/<str:pk>/posts/', TaggedPostListView.as_view()),
    path('tag/<str:pk>/comments/', TaggedCommentListView.as_view()),
]

