from django.contrib.auth.models import User

from django.db import models

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    content = models.TextField(max_length=5000, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT, related_name='posts')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']