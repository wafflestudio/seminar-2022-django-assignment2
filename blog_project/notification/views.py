from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Notification
from .serializers import NotificationSerializer
from .pagination import NotificationPagination

from user.permissions import IsAuthorOrReadOnly

# Create your views here.


class NotificationList(APIView):

    permission_classes = (IsAuthorOrReadOnly, )
    pagination_class = NotificationPagination

    def get(self, request, format=None):
        current_user = request.user
        notifications = Notification.objects.filter(
            notify_to__id=current_user.id)
        serializer = NotificationSerializer(
            notifications, many=True, context={'request': request}
        )
        return Response(data=serializer.data, status=status.HTTP_200_OK)


def create_notification(notify_from, notify_to, notification_type, post=None, comment=None):

    notification = Notification.objects.create(
        notify_from=notify_from,
        notify_to=notify_to,
        notification_type=notification_type,
        post=post,
        comment=comment
    )
    notification.save()
