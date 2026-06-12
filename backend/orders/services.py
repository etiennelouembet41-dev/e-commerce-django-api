from core.models import Notification
from .models import OrderStatusHistory


ALLOWED_ORDER_TRANSITIONS = {
    "pending": ["validated", "cancelled"],
    "validated": ["confirmed", "cancelled"],
    "confirmed": ["processing", "cancelled"],
    "processing": ["importing"],
    "importing": ["delivering"],
    "delivering": ["completed"],
    "completed": [],
    "cancelled": [],
}


def change_order_status(order, new_status, user=None, note=""):
    old_status = order.status

    if new_status not in ALLOWED_ORDER_TRANSITIONS.get(old_status, []):
        raise ValueError(
            f"Transition impossible: {old_status} → {new_status}"
        )

    order.status = new_status
    order.save()

    OrderStatusHistory.objects.create(
        order=order,
        old_status=old_status,
        new_status=new_status,
        changed_by=user,
        note=note,
    )

    Notification.objects.create(
        user=order.user,
        title="Statut de commande mis à jour",
        message=f"Votre commande #{order.id} est maintenant : {new_status}",
    )

    return order