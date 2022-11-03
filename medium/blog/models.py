from django.db import models
from django.contrib.auth.models import User


class Signup(models.Model):
    username = models.CharField(max_length=10)
    password = models.CharField(max_length=20)
    email = models.EmailField()

class Login(models.Model):
    email = models.EmailField()
    password = models.CharField(max_length=20)

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    class Meta:
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_updated = models.BooleanField(default=False)
    class Meta:
        ordering = ['-created_at']

