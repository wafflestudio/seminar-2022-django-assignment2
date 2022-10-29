from django.urls import path
from .views import RegisterView, LoginView, PostListCreateView, PostRetrieveUpdateDestroyView

urlpatterns = [
    path('signin/', RegisterView.as_view()),
    path('login/', LoginView.as_view()),
    path('posts/', PostListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
]