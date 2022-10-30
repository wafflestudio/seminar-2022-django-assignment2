from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver
from django.contrib.auth.hashers import make_password, is_password_usable
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token


class User(User):
    created_at = models.DateTimeField(auto_now=True)


@receiver(pre_save, sender=User)
def password_hashing(instance, **kwargs):
    if is_password_usable(instance.password):
        instance.password = make_password(instance.password)


@receiver(post_save, sender=User)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class Tag(models.Model):
    content = models.CharField(max_length=100, blank=True, primary_key=True)


class Post(models.Model):
    title = models.CharField(max_length=200, blank=True)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now_add=True)
    description = models.TextField(blank=True)
    email = models.EmailField(max_length=200, blank=True)
    read_time = models.IntegerField(default=0)
    like = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='post_tags', through="TagToPostComment")

    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post_id = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='post',
                                db_column='post_id',
                                default=None)
    created_at = models.DateTimeField(auto_now=True)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, default=None, on_delete=models.PROTECT)
    updated_at = models.DateTimeField(auto_now_add=True)
    is_updated = models.BooleanField(default=False)
    content = models.TextField(blank=True)
    like = models.IntegerField(default=0)
    tags = models.ManyToManyField('Tag', related_name='comment_tags', through='TagToPostComment')

    class Meta:
        ordering = ['-created_at']


class TagToPostComment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, null=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
