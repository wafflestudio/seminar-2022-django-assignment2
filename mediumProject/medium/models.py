from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.jpg')


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_updated = models.BooleanField(default=False)



