from django.urls import path
from .views import *

urlpatterns = [
    path('register/', RegisterView.as_view()),
    path('login/', UserLoginView.as_view()),
    path('user/<int:pk>', UserView.as_view()),
    path('post/', PostListView.as_view()),
    path('post/<int:pk>', PostDetailView.as_view()),
    path('post/<int:pk>/comment', CommentListView.as_view()),
    path('post/<int:ppk>/comment/<int:cpk>', CommentRetrieveUpdateDeleteView.as_view())
]