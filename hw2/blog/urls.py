from django.urls import path, include
from rest_framework.routers import DefaultRouter
from blog.views import PostViewSet, CommentViewSet
from . import views

router = DefaultRouter()
router.register(r'posts', PostViewSet, basename="post")
router.register(r'comments', CommentViewSet, basename="comment")

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', views.UserSignUpView.as_view()),
    path('signin/', views.UserSignInView.as_view()),
    path('posts/<int:pk>/comments', views.PostCommentListView.as_view()),
]
