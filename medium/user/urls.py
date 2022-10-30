from django import urls

from user import views as user_views

urlpatterns = [
    urls.path("signup/", user_views.SignUpView.as_view()),
    urls.path("login/", user_views.LoginView.as_view()),
]
