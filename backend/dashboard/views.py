from django.shortcuts import render

from django.db.models import Sum,Count,Avg, CharField
from django.db.models.functions import TruncMonth

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action

from orders.models import Order
from cars.models import Car
from ai_assistant.models import AIQuestion
from imports.models import ImportInfo

from django.db.models.functions import Cast
# Create your views here.


class DashboardStatsView(APIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        
        total_ai_questions=AIQuestion.objects.count()

        frequent_ai_questions = (
            AIQuestion.objects
            .annotate(question_text=Cast("question", CharField(max_length=255)))
            .values("question_text")
            .annotate(total=Count("id"))
            .order_by("-total")[:5]
        )
        
        most_recommended_cars=(
            AIQuestion.objects.values(
                "recommended_cars__brand",
                "recommended_cars__model"
                
            )
            .exclude(recommended_cars=None)
            .annotate(total=Count("id"))
            .order_by("-total")[:10]
            
        )
        
        total_revenue=(
            Order.objects.filter(payment_status="paid").aggregate(total=Sum("total_price"))
        )
        
        total_orders=Order.objects.count()

        available_cars=Car.objects.filter(
            is_available=True
        ).count()

        sold_cars=Car.objects.filter(
            is_sold=True
        ).count()

        importing_cars=ImportInfo.objects.exclude(
            status="delivered"
        ).count()

        monthly_sales=(
            Order.objects.filter(payment_status="paid")
                .annotate(month=TruncMonth("created_at"))
                .values("month")
                .annotate(total=Sum("total_price"))
                .order_by("month")
        )
        
        sales_by_city=(
            Order.objects.values("delivery_city__city__name") 
                .annotate(total=Count("id"))
                .order_by("-total")
        )
        
        #dashboard avancé
        payments_received=(
            Order.objects.filter(payment_status__in=["paid", "deposit_paid"])
            .aggregate(total=Sum("total_price"))
        )
        
        sales_by_origin_country=(
            Order.objects.values("car__origin_country__name")
            .annotate(total_orders=Count("id"), revenue=Sum("total_price"))
            .order_by("-total_orders")
        )
        
        sales_by_race_type=(
            Order.objects.values("car__race_type")
            .annotate(total_orders=Count("id"), revenue=Sum("total_price"))
            .order_by("-total_orders")
        )
        
        top_selling_cars=(
            Order.objects.values("car__brand", "car__model")
            .annotate(total_orders=Count("id"), revenue=Sum("total_price"))
            .order_by("-total_orders")[:10]
            
        )
        
        return Response(
            {
                "total_revenue":total_revenue,
                "total_orders":total_orders,
                "available_cars":available_cars,
                "sold_cars":sold_cars,
                "importing_cars":importing_cars,
                "monthly_sales":monthly_sales,
                "sales_by_city":sales_by_city,
                
                "total_ai_questions":total_ai_questions,
                "frequent_ai_questions":frequent_ai_questions,
                "most_recommended_cars":most_recommended_cars,
                
                "payments_received":payments_received,
                "sales_by_origin_country":sales_by_origin_country,
                "sales_by_race_type":sales_by_race_type,
                "top_selling_cars":top_selling_cars,
                
                
                
                
            }
        )
        
@action(detail=True, methods=["post"], url_path="mark-as-read")
def mark_as_read(self, request, pk=None):
    notification = self.get_object()
    notification.is_read = True
    notification.save()
    return Response({
        "message": "Notification marked as read"
    })