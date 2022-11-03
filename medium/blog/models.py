from django.db import models
from user.models import User

# Create your models here.


class Post(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField(null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    summary = models.CharField(max_length=300, null=True)
    like_count = models.IntegerField(default=0)
    read_time = models.IntegerField(null=True)
    tag = models.ManyToManyField('Tag', related_name='tag_post', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey('Post', related_name='comments', on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField(max_length=200)
    is_updated = models.BooleanField(default=False)
    is_activated = models.BooleanField(default=True)
    like_count = models.IntegerField(default=0)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True)
    tag = models.ManyToManyField('Tag', related_name='tag_comment', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.content + "created by" + self.created_by.__str__()


class Tag(models.Model):
    tag_name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tag_name
