from django.urls import path
from .views import PostListCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
]