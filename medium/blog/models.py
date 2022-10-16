from email.policy import default

from django.contrib.auth.models import User
from django.db import models


class Post(models.Model):
    pid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=50)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    content = models.TextField("CONTENT")
    url = models.URLField(blank=True)

    class Meta:
        verbose_name = "post"
        verbose_name_plural = "posts"
        db_table = "posts"
        ordering = ("-created_at",)

    def __str__(self):
        return self.title


class Comment(models.Model):
    cid = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created_by = models.ForeignKey(User, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField(default=False)
    content = models.TextField("CONTENT")
    num_like = models.IntegerField(default=0)
    num_dislike = models.IntegerField(default=0)

    class Meta:
        verbose_name = "comment"
        verbose_name_plural = "comments"
        db_table = "comments"
        ordering = ("-created_at",)
