from django.conf import settings
from django.core.mail import send_mail

def send_order_confirmation_email(order):
    subject=f"Confirmation commande #{order.id}"

    message=f""" 
Bonjour {order.user.first_name or order.user.username},

Votre commande a bien été créée.

Voiture:{order.car.brand} {order.car.model}
Ville de Livraison : {order.delivery_city.name}
Prix Total: {order.total_price} $
Status: {order.status}

Merci pour votre confiance

Le Vikings Cars 

"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [order.user.email],
        fail_silently=False,
    )

def send_payment_success_email(order):
    subject=f"Paiement confirmé - Commande #{order.id}"

    message=f"""
Bonjour  {order.user.first_name or order.user.username},

Votre paiement a bien été confirmé.

Voiture reservée : {order.car.brand}  {order.car.model}
Statut Paiement : {order.payment_status}
Total : {order.total_price} $

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