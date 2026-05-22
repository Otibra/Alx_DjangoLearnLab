from django.db import models

# Create your models here.
from django.conf import settings
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Notification(models.Model):
    # User receiving the notification
    recipient = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="notifications"
    )

    # User who performed the action
    actor = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="sent_notifications"
    )

    # Description of the action
    verb = models.CharField(max_length=255)

    # GenericForeignKey setup
    target_content_type = models.ForeignKey(
        ContentType,
        on_delete=models.CASCADE
    )
    target_object_id = models.PositiveBigIntegerField()

    # The actual related object
    target = GenericForeignKey(
        "target_content_type",
        "target_object_id"
    )

    # Notification metadata
    timestamp = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ["-timestamp"]

    def __str__(self):
        return f"{self.actor} {self.verb} ({self.recipient})"
    