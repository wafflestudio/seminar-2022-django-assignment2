from . import views
from django.urls import path


urlpatterns = [
    path("signup/", views.SignUpView.as_view(), name="signup"),
    path("login/", views.LoginView.as_view(), name="login"),
    path('profile/', views.ProfileView.as_view(), name="profile"),
]
