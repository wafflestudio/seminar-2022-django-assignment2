from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, email, password, first_name, last_name):
        user = self.model(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.set_password(password)
        user.is_staff = False
        user.is_superuser = False
        user.username = email
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, first_name, last_name):
        user = self.create_user(email=email, password=password)
        user.first_name = first_name
        user.last_name = last_name
        user.is_active = True
        user.is_staff = True
        user.is_superuser = True
        user.username = email
        user.save(using=self._db)
        return user
