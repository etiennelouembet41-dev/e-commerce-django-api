import stripe
from decimal import Decimal, ROUND_HALF_UP

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from stripe import SignatureVerificationError

from orders.models import Order
from imports.models import ImportInfo

from core.emails import send_payment_success_email
from core.models import Notification
from core.realtime import send_realtime_notification
from core.activity import create_audit_log

from invoices.services import create_invoice_for_order


def money_to_cents(amount):
    return int(
        (amount * Decimal("100")).quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP
        )
    )


class CreateCheckoutSessionView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        order_id = request.data.get("order_id")
        payment_type = request.data.get("payment_type", "full")

        if payment_type not in ["deposit", "remaining", "full"]:
            return Response(
                {"error": "Invalid payment type"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.select_related("car", "user").get(
                id=order_id,
                user=request.user,
            )
        except Order.DoesNotExist:
            return Response(
                {"error": "Order not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        if order.payment_status == "paid":
            return Response(
                {"error": "Order already fully paid"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if payment_type == "deposit":
            if order.payment_status != "unpaid":
                return Response(
                    {"error": "Acompte déjà payé"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            amount = order.total_price * Decimal("0.20")
            payment_label = "Acompte 20%"

        elif payment_type == "remaining":
            if order.payment_status != "deposit_paid":
                return Response(
                    {"error": "L’acompte doit être payé avant les 80% restants"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            amount = order.total_price * Decimal("0.80")
            payment_label = "Paiement restant 80%"

        else:
            if order.payment_status != "unpaid":
                return Response(
                    {"error": "Le paiement total est disponible seulement avant l’acompte"},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            amount = order.total_price
            payment_label = "Paiement total"

        amount = amount.quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
        amount_cents = money_to_cents(amount)

        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="payment",
            client_reference_id=str(order.id),
            metadata={
                "order_id": str(order.id),
                "payment_type": payment_type,
                "payment_label": payment_label,
                "paid_amount": str(amount),
            },
            line_items=[
                {
                    "price_data": {
                        "currency": "myr",
                        "product_data": {
                            "name": f"{order.car.brand} {order.car.model} - {payment_label}",
                        },
                        "unit_amount": amount_cents,
                    },
                    "quantity": 1,
                }
            ],
            success_url=(
                f"{settings.FRONTEND_SUCCESS_URL}"
                "?session_id={CHECKOUT_SESSION_ID}"
            ),
            cancel_url=settings.FRONTEND_CANCEL_URL,
        )

        return Response({
            "checkout_url": session.url,
            "payment_type": payment_type,
            "payment_label": payment_label,
            "amount": amount,
        })


@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET,
        )
        print("WEBHOOK RECU:", event["type"])

    except ValueError:
        return HttpResponse("Invalid payload", status=400)

    except SignatureVerificationError:
        return HttpResponse("Invalid signature", status=400)

    except Exception as e:
        print("STRIPE WEBHOOK ERROR:", str(e))
        return HttpResponse("Webhook error", status=400)

    if event["type"] != "checkout.session.completed":
        return HttpResponse(status=200)

    session = event["data"]["object"]
    metadata = session["metadata"] if "metadata" in session else {}

    order_id = metadata["order_id"] if "order_id" in metadata else None
    payment_type = metadata["payment_type"] if "payment_type" in metadata else "full"
    payment_label = metadata["payment_label"] if "payment_label" in metadata else None

    payment_intent = session["payment_intent"] if "payment_intent" in session else None
    paid_amount = Decimal(session["amount_total"]) / Decimal("100")

    if not order_id:
        print("NO ORDER ID FOUND IN STRIPE METADATA")
        return HttpResponse(status=200)

    try:
        order = Order.objects.select_related("user", "car").get(id=order_id)
    except Order.DoesNotExist:
        print("ORDER NOT FOUND:", order_id)
        return HttpResponse(status=200)

    if payment_type == "deposit" and order.payment_status == "deposit_paid":
        return HttpResponse(status=200)

    if payment_type in ["remaining", "full"] and order.payment_status == "paid":
        return HttpResponse(status=200)

    car = order.car

    order.stripe_payment_id = payment_intent
    order.status = "confirmed"

    if payment_type == "deposit":
        order.payment_status = "deposit_paid"
        payment_label = payment_label or "Acompte 20%"

        car.is_reserved = True
        car.is_available = False
        car.is_sold = False

    elif payment_type == "remaining":
        order.payment_status = "paid"
        payment_label = payment_label or "Paiement restant 80%"

        car.is_reserved = False
        car.is_available = False
        car.is_sold = True

    elif payment_type == "full":
        order.payment_status = "paid"
        payment_label = payment_label or "Paiement total"

        car.is_reserved = False
        car.is_available = False
        car.is_sold = True

    else:
        print("UNKNOWN PAYMENT TYPE:", payment_type)
        return HttpResponse(status=200)

    car.save()
    order.save()

    try:
        create_invoice_for_order(
            order=order,
            payment_type=payment_type,
            paid_amount=paid_amount,
        )
    except Exception as e:
        print("INVOICE CREATION ERROR:", str(e))

    try:
        import_info = ImportInfo.objects.get(car=car)
        import_info.status = "confirmed"
        import_info.save(update_fields=["status", "updated_at"])
    except ImportInfo.DoesNotExist:
        print("NO IMPORT INFO FOUND FOR CAR:", car.id)

    Notification.objects.create(
        user=order.user,
        title="Paiement confirmé",
        message=f"Votre {payment_label} pour la commande #{order.id} a été confirmé.",
    )

    user_notification = Notification.objects.filter(
        user=order.user,
        title="Paiement confirmé",
    ).latest("created_at")

    send_realtime_notification(order.user, user_notification)

    create_audit_log(
        action="payment_confirmed",
        message=(
            f"{payment_label} confirmé pour la commande #{order.id} "
            f"du client {order.user.email}. "
            f"Montant payé : {paid_amount} MYR."
        ),
        user=order.user,
        notify_admin=True,
    )

    send_payment_success_email(
        order,
        payment_type=payment_label,
        paid_amount=paid_amount,
    )

    return HttpResponse(status=200)