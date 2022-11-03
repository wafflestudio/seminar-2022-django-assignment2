from django.db import models

from posts.models import Post
from users.models import User
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    written_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False)
    is_updated = models.BooleanField(default=False)
    # order = models.IntegerField(null=)

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '%s' % self.content