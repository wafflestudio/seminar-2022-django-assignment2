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
