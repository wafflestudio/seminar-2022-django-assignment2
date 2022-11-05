from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_updated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']


class Tag(models.Model):
    content = models.CharField(max_length=100, primary_key=True)
    posts = models.ManyToManyField(Post, related_name='tags', blank=True)
    comments = models.ManyToManyField(Comment, related_name='tags', blank=True)
