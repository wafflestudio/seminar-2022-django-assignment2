from re import T
from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class BlogUser(AbstractUser):

    # profile
    nickname = models.CharField(max_length=20)
    short_bio = models.CharField(max_length=100)
    photo = models.ImageField()
    url = models.URLField()

    # following, follower
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

    @property
    def post_count(self):
        return self.posts.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()

    def __str__(self):
        return self.username


class Post(models.Model):

    created_by = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    summary_for_list_api = models.CharField(max_length=300, null=True)
    n_min_read = models.IntegerField()
    member_only = models.BooleanField()
    create_tag = models.CharField(max_length=200)
    tag = models.ManyToManyField('Tag', related_name='tag_by_post')

    @property
    def clapse_count(self):
        return self.clapses.all().count()

    @property
    def comment_count(self):
        return self.comments.all().count()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['-created_at']


class Comment(models.Model):

    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True)
    created_by = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, null=True)
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
        BlogUser, on_delete=models.CASCADE, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.created_by.__str__() + "clapsed to" + self.post.__str__()


class Tag(models.Model):

    name = models.CharField(max_length=30)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Notification(models.Model):

    TYPE_CHOICES = (
        ('clapse', 'Clapse'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    notify_from = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, related_name='notify_from')
    notify_to = models.ForeignKey(
        BlogUser, on_delete=models.CASCADE, related_name='notify_to')
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.notify_from.__str__() + " notified " + self.notify_to.__str__()
