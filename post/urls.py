from django.urls import path
from .views import PostList, PostDetail, CommentList, TagPostList, TagCommentList, UserCreate, LoginView

urlpatterns = [
    path('register/', UserCreate.as_view()),
    path('login/', LoginView.as_view()),
    path('post/', PostList.as_view()),
    path('post/<int:pk>/', PostDetail.as_view()),
    path('post/<int:pk>/comment/', CommentList.as_view()),
    path('tag/post/', TagPostList.as_view()),
    path('tag/comment/', TagCommentList.as_view())
]
