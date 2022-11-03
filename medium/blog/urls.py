from django.urls import path
from . import views

urlpatterns = [
    path('post/', views.PostListView.as_view()),
    path('post/<int:pk>/', views.PostDetailView.as_view()),
    path('post/<int:pk>/comment/', views.CommentListCreateView.as_view()),
    path('post/<int:pid>/comment/<int:cid>/', views.CommentUpdateDeleteView.as_view()),
    path('tag/<str:tag_name>/post/', views.TagPostListView.as_view()),
    path('tag/<str:tag_name>/comment/', views.TagCommentListView.as_view()),
    path('tag/', views.TagListView.as_view()),
]
