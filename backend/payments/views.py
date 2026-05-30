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
            amount=order.total_price * 0.20
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
                            "name":f"{order.car.brand} {order.card.model}",
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
def stripe_webhook(request):#c'est la partie la plus important "Le paiement a réussi." via stripe_webhook
        payload=request.body
        sig_header=request.META.get("HTTP_STRIPE_SIGNATURE")
        
        try:
            event=stripe.Webhook.construct_event(
                payload,
                sig_header,
                settings.STRIPE_WEBHOOK_SECRET
            )
        except ValueError:
            return HttpResponse(status=400)
        except stripe.error.SignatureVerificationError:
            return HttpResponse(status=400)
        
        if event["type"]=="checkout.session.completed":
            session=event["data"]["object"]

            order_id=session.get("metadata",{}).get("order_id")
            payment_type=session.get("metadata",{}).get("payment_type")

            try:
                order=Order.objects.get(id=order_id)
                order.stripe_payment_id=session.get("payment_intent")

                if payment_type=="deposit":
                    order.payment_status="deposit_paid"
                else:
                    order.payment_status="paid"
                
                order.status="confirmed"
                
                order.car.is_reserved=True
                order.car.is_available=False
                order.car.save()

                order.save()
                
                send_payment_success_email(order)
            
            except Order.DoesNotExist:
                pass
            
        return HttpResponse(status=200)
                
            
            