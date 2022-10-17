from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.


class User(AbstractUser):

    nickname = models.CharField(max_length=20, null=True)
    short_bio = models.CharField(max_length=200, null=True)
    photo = models.ImageField(null=True)
    url = models.URLField(null=True)
    followers = models.ManyToManyField("self", blank=True)
    following = models.ManyToManyField("self", blank=True)

    @property
    def post_count(self):
        return self.post.all().count()

    @property
    def followers_count(self):
        return self.followers.all().count()

    @property
    def following_count(self):
        return self.following.all().count()
