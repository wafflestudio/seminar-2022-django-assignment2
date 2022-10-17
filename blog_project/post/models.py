from django.db import models
from user.models import User

# Create your models here.


class Post(models.Model):
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    summary_for_listing = models.CharField(max_length=300, null=True)
    n_min_read = models.IntegerField(null=True)
    create_tag = models.CharField(max_length=200, null=True)
    tag = models.ManyToManyField('Tag', related_name='tag_by_post')

    @property
    def clapse_count(self):
        return self.clapse.all().count()

    @property
    def comment_count(self):
        return self.comment.all().count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_updated = models.BooleanField()
    content = models.TextField()
    parent_comment = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True)
    create_tag = models.CharField(max_length=200, null=True)
    tag = models.ManyToManyField('Tag', related_name='tag_by_comment')

    def __str__(self):
        return self.content


class Clapse(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.__str__() + "clapsed to" + self.post.__str__()


class Tag(models.Model):
    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.name
