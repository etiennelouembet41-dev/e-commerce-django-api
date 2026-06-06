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
        read_only_fields=(
            "user",
            "car_price",
            "import_fees",
            "delivery_fees",
            "total_price",
            "payment_status",
            "stripe_payment_id",
        )

class OrderDetailSerializer(serializers.ModelSerializer):
    car_name=serializers.SerializerMethodField()
    delivery_city_name=serializers.SerializerMethodField()
    import_status=serializers.SerializerMethodField()

    class Meta:
        model=Order
        fields="__all__"
        
    def get_car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"
    
    def get_delivery_city_name(self,obj):
        return obj.delivery_city.name

    def get_import_status(self, obj):
        import_info = obj.car.import_info.first()
        return import_info.status if import_info else None


class OrderListSerializer(serializers.ModelSerializer):
    car_name = serializers.SerializerMethodField()
    delivery_city_name = serializers.SerializerMethodField()
    import_status = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_car_name(self, obj):
        return f"{obj.car.brand} {obj.car.model}"

    def get_delivery_city_name(self, obj):
        return obj.delivery_city.name

    def get_import_status(self, obj):
        import_info = getattr(obj.car, "import_info", None)

        if import_info:
            return import_info.status

        return None

