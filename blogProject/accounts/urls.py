from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from accounts import views

urlpatterns = [
    path('signup/', views.SignUpView.as_view()),
    path('login/', views.LogInView.as_view()),
    # path('api-auth/', include('rest_framework.urls')),
]
