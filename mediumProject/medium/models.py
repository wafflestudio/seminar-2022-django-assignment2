from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    post_id = models.AutoField(primary_key=True)
    created_by = models.ForeignKey(User, related_name='post', on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=128)
    description = models.TextField()
    image = models.ImageField(upload_to='post/', default='default.jpg')
    tag = models.ManyToManyField('Tag', through='TagToPost')
    likes = models.ManyToManyField(User, related_name='like_post', blank=True)


class Comment(models.Model):
    comment_id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, related_name='comment', on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField()
    is_updated = models.BooleanField(default=False)
    tag = models.ManyToManyField('Tag', through='TagToComment')
    likes = models.ManyToManyField(User, related_name='like_comment', blank=True)


class Tag(models.Model):
    content = models.CharField(max_length=50, primary_key=True, blank=True)


class TagToPost(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)


class TagToComment(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)




