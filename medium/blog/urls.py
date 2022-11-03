from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from blog.views import SignUpView, LoginView, PostListCreateView, PostRetrieveUpdateDestroyView, CommentListCreateView, CommentRetrieveUpdateDestroyView

urlpatterns = [
    path('signup/', SignUpView.as_view()),
    path('login/', LoginView.as_view()),
    path('post/', PostListCreateView.as_view()),
    path('post/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('post/<int:pk>/comment/', CommentListCreateView.as_view()),
    path('post/<int:pk>/comment/<int:id>/', CommentRetrieveUpdateDestroyView.as_view())
]
