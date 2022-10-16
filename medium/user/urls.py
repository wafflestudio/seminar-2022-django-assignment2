from django import urls
from user import views as user_views

urlpatterns = [
    urls.path("register/", user_views.RegisterView.as_view()),
]
