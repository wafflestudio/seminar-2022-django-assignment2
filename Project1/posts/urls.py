from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostCreateRetrieveUpdateDestroyView, PostListView

urlpatterns = [
    path('posts/list/', PostListView.as_view()),
    path('posts/<str:title>', PostCreateRetrieveUpdateDestroyView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)