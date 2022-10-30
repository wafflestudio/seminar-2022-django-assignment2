from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostListCreateView, PostRetrieveUpdateDestroyView
from .views import CommentListCreateView, CommentUpdateDestroyView, PostByTagListView, CommentByTagListView
from rest_framework.authtoken.views import obtain_auth_token


urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('posts/<int:post_id>/comments/', CommentListCreateView.as_view()),
    path('posts/<int:post_id>/comments/<int:pk>', CommentUpdateDestroyView.as_view()),
    path('comments/<int:pk>/', CommentUpdateDestroyView.as_view()),
    path('tags/<str:tag>/posts/', PostByTagListView.as_view()),
    path('tags/<str:tag>/comments/', CommentByTagListView.as_view()),
    path('api-token-auth/', obtain_auth_token),
]


urlpatterns = format_suffix_patterns(urlpatterns)

