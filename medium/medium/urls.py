from django import urls
from django.contrib import admin

urlpatterns = [
    urls.path("admin/", admin.site.urls),
    urls.path("user/", urls.include("user.urls")),
    urls.path("blog/", urls.include("blog.urls")),
]
