from django.urls import path, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('medium/', include('medium.urls')),
    path('accounts/', include('drf_registration.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
