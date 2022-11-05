from django.urls import path, include
from rest_framework import routers
from .views import PostListAPI, PostViewSets, CommentListAPI, CommentViewSets, api_root

post_list = PostListAPI.as_view()

post_create = PostViewSets.as_view({
    'post': 'create'
})
post_detail = PostViewSets.as_view({
    'get': 'retrieve',
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})

comment_list = CommentListAPI.as_view()
comment_create = CommentViewSets.as_view({
    'post': 'create',
})
comment_detail = CommentViewSets.as_view({
    'put': 'update',
    'patch': 'partial_update',
    'delete': 'destroy'
})


urlpatterns = [
    path('', api_root),
    path('posts_preview/', post_list, name='post-list'),
    path('posts/', post_create, name='post-create'),
    path('posts/<int:pk>/', post_detail, name='post-detail'),
    path('comments_preview/', comment_list, name='comment-list'),
    path('comments/', comment_create, name='comment-create'),
    path('comments/<int:pk>/', comment_detail, name='comment-detail'),
]