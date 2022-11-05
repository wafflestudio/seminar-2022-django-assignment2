from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField(null=False)
    description_preview = models.TextField(max_length=300, default="")

    class Meta:
        pass

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    created = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=300, null=False)
    is_updated = models.BooleanField(default=False, null=False)

    class Meta:
        pass