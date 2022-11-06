from django.contrib.auth.models import User
from django.db import models
from rest_framework.authtoken.models import Token


# Create your models here.
class Tag(models.Model):
    content = models.CharField(max_length=50, primary_key=True)


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    reading_time = models.PositiveIntegerField(null=True, blank=True)
    tags = models.ManyToManyField(Tag, related_name='posts', editable=False)
    description = models.TextField()

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False, editable=False)
    tags = models.ManyToManyField(Tag, related_name='comments', editable=False)
    content = models.TextField()

    class Meta:
        ordering = ['-created_at']


class UserFollowing(models.Model):
    user = models.ForeignKey(User, related_name='following', on_delete=models.CASCADE, editable=False)
    following_user = models.ForeignKey(User, related_name='followers', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = property(lambda self: self.user)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user', 'following_user'], name='can follow the same user once'),
        ]
