from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='posts/', default='default.jpg')
