from django.db import models
from django.contrib.auth.models import AbstractBaseUser
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=100, blank=True, default='')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, editable=False, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    description = models.TextField()
    email = models.EmailField(max_length=100)

    class Meta:
        ordering = ['created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.SET_DEFAULT, editable=False, null=True, default=None)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_updated = models.BooleanField(editable=False, default=False)

    class Meta:
        ordering = ['created_at']

    def save(self, *args, **kwargs):
        if self.pk is not None:
            self.is_updated = True
        super().save(*args, **kwargs)



