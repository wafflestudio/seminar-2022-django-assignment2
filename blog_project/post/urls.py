from django.urls import path
from .views import PostList, PostDetail, \
    CommentList, CommentDetail, \
    ClapseList, UnClapseList, \
    TagPostList, TagCommentList


urlpatterns = [
    path('', PostList.as_view()),
    path('<int:pk>/', PostDetail.as_view()),
    path('<int:pk>/comment/', CommentList.as_view()),
    path('<int:pk>/comment/<int:pk2>/', CommentDetail.as_view()),
    path('<int:pk>/clapse/', ClapseList.as_view()),
    path('<int:pk>/unclapse/', UnClapseList.as_view()),
    path('tag/post/', TagPostList.as_view()),
    path('tag/comment/<str:tagname>', TagCommentList.as_view())
]
