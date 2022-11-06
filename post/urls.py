from django.urls import path
from django.conf.urls import url
from .views import PostList, PostCreate, PostDetail, CommentListCreateView, CommentDetailView
# Blog 목록 보여주기
urlpatterns = [
    path("list", PostList.as_view()),
    path("create", PostCreate.as_view()),
    path("<int:pk>/detail", PostDetail.as_view()),
    path("<int:pk>/comment", CommentListCreateView.as_view()),
    path("<int:pk>/comment/<int:id>", CommentDetailView.as_view())
]