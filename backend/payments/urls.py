from django.urls import path
from .views import CreateCheckoutSessionView, stripe_webhook

urlpatterns = [
    path("create_checkout_session/", CreateCheckoutSessionView.as_view()),
    path("webhook/", stripe_webhook),
]
