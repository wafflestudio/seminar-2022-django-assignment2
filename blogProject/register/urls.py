from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from .views import *

urlpatterns = [
    path('signup/', RegisterAPI.as_view()),
    path('token/<int:user_id>/', GetTokenAPI.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)