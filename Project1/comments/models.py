import posts.models
from django.db import models

from users.models import User
# Create your models here.
class Comment(models.Model):
    post = models.ForeignKey(posts.models.Post, related_name='comments', on_delete=models.CASCADE)
    written_by = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(null=False)
    is_updated = models.BooleanField(default=False)
    tags = models.ManyToManyField("tags.Tag", through="TagToComment")

    class Meta:
        ordering = ['-created_at']

    def __unicode__(self):
        return '%s' % self.content

class TagToComment(models.Model):
    tag = models.ForeignKey("tags.Tag", on_delete=models.CASCADE)
    comment = models.ForeignKey("comments.Comment", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['created_at']