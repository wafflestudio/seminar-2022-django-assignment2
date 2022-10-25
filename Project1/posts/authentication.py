#The following example will authenticate any incoming request
#as the user given by the username in a custom request header named 'X-USERNAME'.

from django.contrib.auth.models import User
from rest_framework import authentication
from rest_framework import exceptions

class PostAuthentication(authentication.BaseAuthentication):
    def authenticate(self, request):
        username = request.META.get('HTTP_X_USERNAME')
        if not username:
            return None

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise exceptions.AuthenticationFailed('No such user')

        return (user, None)