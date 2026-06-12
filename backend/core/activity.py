from django.contrib.auth import get_user_model

from core.models import Notification, AuditLog
from core.realtime import send_realtime_notification

User = get_user_model()


def notify_admins(title, message):
    admins = User.objects.filter(role="admin")

    for admin in admins:
        notification = Notification.objects.create(
            user=admin,
            title=title,
            message=message,
        )

        send_realtime_notification(admin, notification)


def create_audit_log(action, message, user=None, notify_admin=True):
    log = AuditLog.objects.create(
        user=user,
        action=action,
        message=message,
    )

    if notify_admin:
        notify_admins(
            title="Activité système",
            message=message,
        )

    return log