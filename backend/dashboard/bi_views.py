from django.db.models import Sum, Count, Avg
from django.db.models.functions import TruncMonth
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated

from orders.models import Order
from cars.models import Car
from users.models import User


class BusinessIntelligenceView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        paid_statuses = ["paid", "deposit_paid"]

        total_revenue = (
            Order.objects.filter(payment_status__in=paid_statuses)
            .aggregate(total=Sum("total_price"))["total"]
            or 0
        )

        total_orders = Order.objects.count()

        average_order_value = (
            Order.objects.aggregate(avg=Avg("total_price"))["avg"]
            or 0
        )

        paid_orders = Order.objects.filter(
            payment_status__in=paid_statuses
        ).count()

        revenue_by_month = list(
            Order.objects.filter(payment_status__in=paid_statuses)
            .annotate(month=TruncMonth("created_at"))
            .values("month")
            .annotate(revenue=Sum("total_price"), orders=Count("id"))
            .order_by("month")
        )

        sales_by_country = list(
            Order.objects.values("car__origin_country__country")
            .annotate(
                orders=Count("id"),
                revenue=Sum("total_price")
            )
            .order_by("-revenue")
        )

        sales_by_race_type = list(
            Order.objects.values("car__race_type")
            .annotate(
                orders=Count("id"),
                revenue=Sum("total_price")
            )
            .order_by("-revenue")
        )

        top_cars = list(
            Order.objects.values("car__brand", "car__model")
            .annotate(
                orders=Count("id"),
                revenue=Sum("total_price")
            )
            .order_by("-revenue")[:10]
        )

        top_customers = list(
            Order.objects.values("user__email")
            .annotate(
                orders=Count("id"),
                total_spent=Sum("total_price")
            )
            .order_by("-total_spent")[:10]
        )

        inventory_value = (
            Car.objects.filter(is_available=True)
            .aggregate(total=Sum("price"))["total"]
            or 0
        )

        cars_by_status = {
            "available": Car.objects.filter(is_available=True).count(),
            "reserved": Car.objects.filter(is_reserved=True).count(),
            "sold": Car.objects.filter(is_sold=True).count(),
        }

        return Response({
            "kpis": {
                "total_revenue": total_revenue,
                "total_orders": total_orders,
                "average_order_value": average_order_value,
                "paid_orders": paid_orders,
                "total_users": User.objects.count(),
                "inventory_value": inventory_value,
            },
            "revenue_by_month": revenue_by_month,
            "sales_by_country": sales_by_country,
            "sales_by_race_type": sales_by_race_type,
            "top_cars": top_cars,
            "top_customers": top_customers,
            "cars_by_status": cars_by_status,
        })