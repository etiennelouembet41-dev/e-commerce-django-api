from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer


def send_realtime_notification(user, notification):
    channel_layer = get_channel_layer()

    async_to_sync(channel_layer.group_send)(
        f"user_notifications_{user.id}",
        {
            "type": "send_notification",
            "notification": {
                "id": notification.id,
                "title": notification.title,
                "message": notification.message,
                "is_read": notification.is_read,
                "created_at": notification.created_at.isoformat(),
            },
        }
    )