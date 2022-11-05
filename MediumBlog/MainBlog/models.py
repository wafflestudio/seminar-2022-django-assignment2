from django.db import models

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    bookmarks = models.ManyToManyField('Post', related_name='bookmarks')
    clap_posts = models.ManyToManyField('Post', related_name='claps')
    clap_comments = models.ManyToManyField('Comment', related_name='claps')
    responded_posts = models.ManyToManyField('Post', related_name='responses')
    responded_comments = models.ManyToManyField('Comment', related_name='responses')
#    subscribers = models.ManyToManyField('self', related_name='subscribers')


class Post(models.Model):
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField()
    is_updated = models.BooleanField(default=False)

    published_at = models.DateTimeField()
    is_published = models.BooleanField(default=False)

    title = models.CharField(max_length=100)
    content = models.TextField()

    tags = models.ManyToManyField('PostTag')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)

    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField()
    is_updated = models.BooleanField(default=False)

    content = models.TextField()

    tags = models.ManyToManyField('CommentTag')


class PostTag(models.Model):
    content = models.CharField(max_length=100, unique=True, primary_key=True)


class CommentTag(models.Model):
    content = models.CharField(max_length=100, unique=True, primary_key=True)

