from django.db import models
from django.db.models.signals import post_delete, pre_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import AbstractUser, PermissionsMixin
from MediumProject import settings
from blog.managers import UserManager


@receiver(post_delete, sender='blog.Post')
def delete_post_tag(sender, instance, **kwargs):
    tag_id = instance.tag_id
    if PostTag.objects.filter(content=tag_id).count() == 0:
        return
    tag = instance.tag
    if tag.post_set.all().count() == 0:
        tag.delete()

@receiver(post_delete, sender='blog.Comment')
def delete_comment_tag(sender, instance, **kwargs):
    tag_id = instance.tag_id
    if CommentTag.objects.filter(content=tag_id).count() ==0:
        return
    tag = instance.tag
    if tag.comment_set.all().count() == 0:
        tag.delete()


class MyUser(AbstractUser):
    email = models.EmailField(unique=True)
    USERNAME_FIELD = 'email'
    first_name = models.CharField(max_length=20)
    last_name = models.CharField(max_length=20)
    created = models.DateTimeField(auto_now_add=True)
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        return self.email.split("@")[0]+"/"+self.last_name


def get_sentinel_user():
    return MyUser.objects.get_or_create(username='(unknown)')[0]


class Post(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user)
    )
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    content = models.TextField(max_length=3000, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    tag = models.ForeignKey('PostTag', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created']


class Comment(models.Model):
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET(get_sentinel_user)
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE
    )
    content = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    tag = models.ForeignKey('CommentTag', on_delete=models.DO_NOTHING)

    class Meta:
        ordering = ['-created']


class PostTag(models.Model):
    content = models.CharField(max_length=10, primary_key=True, blank=True, default="none")


class CommentTag(models.Model):
    content = models.CharField(max_length=10, primary_key=True, blank=True, default="none")
