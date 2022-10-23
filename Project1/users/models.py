from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

def upload_to(instance, filename):
    return f'images/{filename}'.format(filename=filename)

class User(AbstractUser):
    profile_photo = models.ImageField(upload_to = upload_to, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['username']

# User랑 User의 팔로잉은 따로 관리하기 위해서 분리하는 것이 좋지 않을까?
class UserFollowing(models.Model):
    user_id = models.ForeignKey("User", related_name="following", on_delete=models.CASCADE)
    following_user_id = models.ForeignKey("User", related_name="followers", on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['user_id', 'following_user_id'], name="unique_followers")
        ]

        ordering = ['-created_at']

    def __str__(self):
        return f"{self.user_id} follows {self.following_user_id}"