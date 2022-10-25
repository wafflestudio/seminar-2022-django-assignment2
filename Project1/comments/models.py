from django.db import models

from posts.models import Post
from users.models import User
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    written_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False)
    is_updated = models.BooleanField(default=Fasle)
    order = models.IntegerField()

    class Meta:
        unique_together = ['post_id', 'order']
        ordering = ['order']
    def __unicode__(self):
        return '%s' % self.content