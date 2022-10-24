from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from . import models, serializers
# Create your views here.


class NotificationList(APIView):

    authentication_classes = ()
    permission_classes = ()

    def get(self, request, format=None):
        user = request.user
        notifications = models.Notification.objects.filter(notify_to=user)
        serializer = serializers.NotificationSerializer(
            notifications, many=True, context={'request': 'request'}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(notify_from, notify_to, notification_type, post=None, comment=None):
    notification = models.Notification.objects.create(
        notify_from=notify_from,
        notify_to=notify_to,
        notification_type=notification_type,
        post=post,
        comment=comment
    )
    notification.save()

    action = ''
    if notification_type == 'clapse':
        action = 'clapsed your post'
    elif notification_type == 'comment':
        action = 'commented on your post'
    elif notification_type == 'follow':
        action = 'followed you'

    url = "v1/"
