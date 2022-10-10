from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField()

    create_tag = models.CharField(max_length=200)
    tag = models.ManyToManyField('Tag', related_name='tag_by_post')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.CharField(max_length=100)

    create_tag = models.CharField(max_length=200)
    tag = models.ManyToManyField('Tag', related_name='tag_by_comment')

    def __str__(self):
        return self.content


class Tag(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.name
