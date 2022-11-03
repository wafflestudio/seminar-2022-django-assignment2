from django.urls import path, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import PostRetrieveUpdateDestroyView, PostListView, PostCreateView

urlpatterns = [
    path('<int:post_id>/comments/', include('comments.urls')),
    path('list/', PostListView.as_view()),
    path('new-story', PostCreateView.as_view()),
    path('<int:post_id>/', PostRetrieveUpdateDestroyView.as_view(), name='post-detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)