from django.db import models
from user.models import User
from post.models import Post

# Create your models here.


class Notification(models.Model):
    TYPE_CHOICES = (
        ('clapse', 'Clapse'),
        ('comment', 'Comment'),
        ('follow', 'Follow')
    )

    created_at = models.DateTimeField(auto_now_add=True)
    notify_from = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notify_from'
    )
    notify_to = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='notify_to'
    )
    notification_type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, null=True, blank=True
    )
    comment = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.notify_from.__str__() + " notified " + self.notify_to.__str__()
