from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token


# Create your models here.
# class UserInfo(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     id = models.CharField(max_length=20)
#     password = models.CharField(max_length=50)
#     name = models.CharField(max_length=20)

@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class BlogPost(models.Model):
    pid = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.CharField(max_length=1000)


class BlogComment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=1000)
    is_updated = models.BooleanField(null=True)