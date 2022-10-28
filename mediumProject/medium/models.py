from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(default=timezone.now) #update time?
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.jpg')
