from django.db import models

from users.models import User

# Create your models here.
class Post(models.Model):
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    title = models.CharField(max_length=100, null=False)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tags = models.ManyToManyField('TagAtPost', blank=True)
    class Meta:
        ordering = ['-created_at']
    def __str__(self):
        return self.title