from django.shortcuts import render
import stripe

from django.conf import settings
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status

from orders.models import Order

from core.emails import send_payment_success_email

from decimal import Decimal

from stripe import SignatureVerificationError

from imports.models import ImportInfo

from core.models import Notification

# Create your views here.

class CreateCheckoutSessionView(APIView):
    permission_classes=[IsAuthenticated]
    
    

    def post(self, request):
        order_id=request.data.get("order_id") #le frontend envoi et on récupère la commande 
        payment_type=request.data.get("payment_type", "full")
        
        try: 
            order=Order.objects.get(id=order_id, user=request.user)#on récupère la voiture + prix depuis oracle
        except Order.DoesNotExist:
            return Response(
                {"error":"Order not found"},
                status=status.HTTP_404_NOT_FOUND
            )
        
        if payment_type=="deposit":
            amount = order.total_price * Decimal("0.20")
        else:
            amount=order.total_price#on décide combien payer parfois acompte c'est selon le projet en tout cas
            
        amount_cents=int(amount * 100)

        session=stripe.checkout.Session.create(#c'est le moment important on demande à stripe "Crée une page de paiement pour ce montant." et stripe retourne checkout_url
            payment_method_types=["card"],
            mode="payment",
            client_reference_id=str(order.id),
            metadata={
                "order_id":str(order.id),
                "payment_type":payment_type,
                
            },
            line_items=[
                {
                    "price_data":{
                        "currency":"myr",
                        "product_data":{
                            "name":f"{order.car.brand} {order.car.model}",
                        },
                        
                        "unit_amount":amount_cents,
                    },
                    "quantity":1,
                }
            ],
            success_url=f"{settings.FRONTEND_SUCCESS_URL}?session_id={{CHECKOUT_SESSION_ID}}",
            cancel_url=settings.FRONTEND_CANCEL_URL,
            
        )
        
        return Response({"checkout_url":session.url})
    
@csrf_exempt
def stripe_webhook(request):
    payload = request.body
    sig_header = request.META.get("HTTP_STRIPE_SIGNATURE")

    try:
        event = stripe.Webhook.construct_event(
            payload,
            sig_header,
            settings.STRIPE_WEBHOOK_SECRET
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

    metadata = session["metadata"]
    payment_intent = session["payment_intent"]

    print("SESSION METADATA:", metadata)
    print("PAYMENT INTENT:", payment_intent)

    order_id = metadata["order_id"]
    payment_type = metadata["payment_type"]

    try:    
        order = Order.objects.get(id=order_id)
    except Order.DoesNotExist:  
        return HttpResponse(status=200)

    order.stripe_payment_id = payment_intent
    order.payment_status = "deposit_paid" if payment_type == "deposit" else "paid"
    order.status = "confirmed"

    car = order.car
    car.is_reserved = True
    car.is_available = False

    if payment_type == "full":
        car.is_sold = True

    
    
    car.save()

    try:
        import_info = ImportInfo.objects.get(car=car)
        import_info.status = "confirmed"
        import_info.save(update_fields=["status", "updated_at"])
        print("IMPORT STATUS UPDATED:", import_info.status)
    except ImportInfo.DoesNotExist:
        print("NO IMPORT INFO FOUND FOR CAR:", car.id)

    order.save()
    
    Notification.objects.create(
        user=order.user,
        title="Paiement confirmé",
        message=f"Votre paiement pour la commande #{order.id} a été confirmé."
    )

    send_payment_success_email(order)

    return HttpResponse(status=200)