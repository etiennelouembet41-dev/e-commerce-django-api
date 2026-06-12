from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

from .tokens import account_activation_token


def send_activation_email(user, request):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = account_activation_token.make_token(user)

    activation_path = reverse(
        "activate-account",
        kwargs={"uidb64": uid, "token": token}
    )

    activation_link = request.build_absolute_uri(activation_path)

    subject = "Activation de votre compte Le Vikings Cars"

    message = f"""
Bonjour {user.first_name or user.username},

Merci pour votre inscription sur Le Vikings Cars.

Pour activer votre compte, cliquez sur le lien ci-dessous :

{activation_link}

Si vous n'êtes pas à l'origine de cette inscription, ignorez cet email.

Le Vikings Cars
"""

    send_mail(
        subject,
        message,
        settings.DEFAULT_FROM_EMAIL,
        [user.email],
        fail_silently=False,
    )