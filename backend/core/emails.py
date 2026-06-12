from django.conf import settings
from django.core.mail import send_mail


def send_order_confirmation_email(order):
    subject = f"Confirmation commande #{order.id}"

    message = f"""
Bonjour {order.user.first_name or order.user.username},

Votre commande a bien été créée.

Voiture : {order.car.brand} {order.car.model}
Ville de livraison : {order.delivery_city.name}
Prix total : {order.total_price} MYR
Statut commande : {order.status}
Statut paiement : {order.payment_status}

Merci pour votre confiance.

Le Vikings Cars
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )


def send_payment_success_email(order, payment_type="paiement total", paid_amount=None):
    paid_amount = paid_amount if paid_amount is not None else order.total_price

    payment_type_lower = str(payment_type).lower()

    if "acompte" in payment_type_lower or "20" in payment_type_lower or payment_type_lower == "deposit":
        subject = f"Acompte 20% confirmé - Commande #{order.id}"
        type_label = "Acompte 20%"
        amount_label = "Montant de l'acompte payé"

    elif "80" in payment_type_lower or "remaining" in payment_type_lower or "solde" in payment_type_lower:
        subject = f"Paiement restant 80% confirmé - Commande #{order.id}"
        type_label = "Paiement restant 80%"
        amount_label = "Montant du paiement restant payé"

    else:
        subject = f"Paiement total confirmé - Commande #{order.id}"
        type_label = "Paiement total"
        amount_label = "Montant total payé"

    message = f"""
Bonjour {order.user.first_name or order.user.username},

Votre paiement a bien été confirmé.

Voiture réservée : {order.car.brand} {order.car.model}
Type de paiement : {type_label}
{amount_label} : {paid_amount} MYR
Prix total de la commande : {order.total_price} MYR
Statut paiement : {order.payment_status}

Nous lançons maintenant le processus d'importation.

Le Vikings Cars
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )