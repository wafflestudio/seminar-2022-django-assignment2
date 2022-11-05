from django.urls import path

from posts import views

urlpatterns = [
    path('', views.PostListView.as_view()),
    path('<int:pk>/', views.PostDetailView.as_view()),
    path('<int:pk>/comments/', views.CommentListView.as_view()),
    # path('<int:pk>/comments/<int:cpk>', views.CommentUpdateView.as_view()),
    # path('<int:pk>/comments/<int:cpk>', views.CommentDestroyView.as_view()),
    path('<int:pk>/comments/<int:cpk>', views.CommentDetailView.as_view())
]
