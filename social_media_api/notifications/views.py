from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
# Create your views here.

class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(
            recipient=request.user
        ).select_related(
            "actor",
            "recipient",
            "target_content_type",
        )

        unread_count = notifications.filter(read=False).count()

        data = []

        for notification in notifications:
            data.append(
                {
                    "id": notification.id,
                    "actor": notification.actor.username,
                    "verb": notification.verb,
                    "target_type": notification.target_content_type.model,
                    "target_id": notification.target_object_id,
                    "read": notification.read,
                    "timestamp": notification.timestamp,
                }
            )

        return Response(
            {
                "unread_count": unread_count,
                "notifications": data,
            },
            status=status.HTTP_200_OK,
        )


class MarkNotificationReadView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, notification_id):
        notification = Notification.objects.filter(
            id=notification_id,
            recipient=request.user,
        ).first()

        if not notification:
            return Response(
                {"detail": "Notification not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        notification.read = True
        notification.save(update_fields=["read"])

        return Response(
            {"detail": "Notification marked as read."},
            status=status.HTTP_200_OK,
        )
    