from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url

#urls for token 발행
urlpatterns = [
    url(r'^rest-auth/', include('rest_auth.urls')),
    url(r'^rest-auth/registration/', include('rest_auth.registration.urls'))
]