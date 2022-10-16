from rest_framework import serializers
from .models import Notification


class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        fields = (
            'created_at',
            'notify_from',
            'notify_to',
            'notification_type',
            'comment'
        )
        model = Notification
