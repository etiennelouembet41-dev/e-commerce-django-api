from rest_framework import serializers 
from .models import Order,OrderItem

class OrderItemSerializers(serializers.ModelSerializer):
    class Meta:
        model=OrderItem
        fields="__all__"
        
class OrderSerializers(serializers.ModelSerializer):
    items=OrderItemSerializers(many=True,read_only=True)
    
    class Meta:
        model=Order
        fields="__all__"
        read_on_fields=(
            "user",
            "car_price",
            "import_fees",
            "delivery_fees",
            "total_price",
            "payment_status",
            "stripe_payment_id",
        )
        
