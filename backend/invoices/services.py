import os

from django.conf import settings
from django.core.files import File
from django.core.mail import EmailMessage

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4

from .models import Invoice


def create_invoice_for_order(order, payment_type, paid_amount):
    if payment_type == "deposit":
        label = "Acompte 20%"
    elif payment_type == "remaining":
        label = "Paiement restant 80%"
    else:
        label = "Paiement total"

    invoice_number = (
        f"INV-{order.id}-{Invoice.objects.count() + 1}"
    )

    invoice = Invoice.objects.create(
        order=order,
        invoice_number=invoice_number,
        payment_type=payment_type,
        amount_paid=paid_amount,
    )

    folder = os.path.join(
        settings.MEDIA_ROOT,
        "invoices"
    )

    os.makedirs(folder, exist_ok=True)

    filename = f"{invoice_number}.pdf"
    filepath = os.path.join(folder, filename)

    pdf = canvas.Canvas(filepath, pagesize=A4)

    width, height = A4

    pdf.setFont("Helvetica-Bold", 18)
    pdf.drawString(
        50,
        height - 60,
        "Le Vikings Cars"
    )

    pdf.setFont("Helvetica", 12)

    pdf.drawString(
        50,
        height - 100,
        f"Facture : {invoice_number}"
    )

    pdf.drawString(
        50,
        height - 130,
        f"Client : {order.user.email}"
    )

    pdf.drawString(
        50,
        height - 160,
        f"Commande : #{order.id}"
    )

    pdf.drawString(
        50,
        height - 190,
        f"Vehicule : {order.car.brand} {order.car.model}"
    )

    pdf.drawString(
        50,
        height - 220,
        f"Type de paiement : {label}"
    )

    pdf.drawString(
        50,
        height - 250,
        f"Montant paye : {paid_amount} MYR"
    )

    pdf.drawString(
        50,
        height - 280,
        f"Prix total commande : {order.total_price} MYR"
    )

    pdf.drawString(
        50,
        height - 340,
        "Merci pour votre confiance."
    )

    pdf.save()

    with open(filepath, "rb") as f:
        invoice.pdf_file.save(
            filename,
            File(f),
            save=True
        )

    if order.user.email:
        email = EmailMessage(
            subject=f"Facture {invoice_number}",
            body=f"""
Bonjour,

Veuillez trouver ci-joint votre facture.

Commande : #{order.id}
Véhicule : {order.car.brand} {order.car.model}
Type de paiement : {label}
Montant payé : {paid_amount} MYR

Merci pour votre confiance.

Le Vikings Cars
""",
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=[order.user.email],
        )

        email.attach_file(invoice.pdf_file.path)

        try:
            email.send()
        except Exception as e:
            print("EMAIL INVOICE ERROR:", str(e))

    return invoice