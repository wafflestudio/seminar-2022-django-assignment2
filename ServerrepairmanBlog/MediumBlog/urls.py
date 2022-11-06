from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from MediumBlog.views import PostPermissionListCreateView, PostListCreateView, SignupView, SigninView, \
    PostRetrieveUpdateDestroyView

urlpatterns = [
    path('posts/', PostPermissionListCreateView.as_view()),
    path('posts/<int:pk>/', PostRetrieveUpdateDestroyView.as_view()),
    path('register/', SignupView.as_view()),
    path('login/', SigninView().as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
