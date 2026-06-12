from rest_framework import serializers
from .models import Order, OrderItem
from invoices.serializers import InvoiceSerializer


class OrderItemSerializers(serializers.ModelSerializer):
    car_name = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = "__all__"

    def get_car_name(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return None


class OrderSerializers(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)
    car_name = serializers.SerializerMethodField()
    delivery_city_name = serializers.SerializerMethodField()
    delivery_address_text = serializers.SerializerMethodField()
    import_status = serializers.SerializerMethodField()
    car_main_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"
        read_only_fields = (
            "user",
            "car_price",
            "import_fees",
            "delivery_fees",
            "total_price",
            "payment_status",
            "stripe_payment_id",
        )

    def get_car_name(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return None

    def get_delivery_city_name(self, obj):
        return obj.delivery_city.name if obj.delivery_city else None

    def get_delivery_address_text(self, obj):
        return obj.delivery_address.address_line if obj.delivery_address else None

    def get_import_status(self, obj):
        import_info = getattr(obj.car, "import_info", None)
        return import_info.status if import_info else None

    def get_car_main_image(self, obj):
        request = self.context.get("request")

        if obj.car and obj.car.main_image:
            image_url = obj.car.main_image.url

            if request:
                return request.build_absolute_uri(image_url)

            return image_url

        return None


class OrderListSerializer(serializers.ModelSerializer):
    invoices = InvoiceSerializer(many=True, read_only=True)
    car_name = serializers.SerializerMethodField()
    delivery_city_name = serializers.SerializerMethodField()
    delivery_address_text = serializers.SerializerMethodField()
    import_status = serializers.SerializerMethodField()
    car_main_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_car_name(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return None

    def get_delivery_city_name(self, obj):
        return obj.delivery_city.name if obj.delivery_city else None

    def get_delivery_address_text(self, obj):
        return obj.delivery_address.address_line if obj.delivery_address else None

    def get_import_status(self, obj):
        import_info = getattr(obj.car, "import_info", None)
        return import_info.status if import_info else None

    def get_car_main_image(self, obj):
        request = self.context.get("request")

        if obj.car and obj.car.main_image:
            image_url = obj.car.main_image.url

            if request:
                return request.build_absolute_uri(image_url)

            return image_url

        return None


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializers(many=True, read_only=True)
    invoices = InvoiceSerializer(many=True, read_only=True)
    car_name = serializers.SerializerMethodField()
    delivery_city_name = serializers.SerializerMethodField()
    delivery_address_text = serializers.SerializerMethodField()
    import_status = serializers.SerializerMethodField()
    car_main_image = serializers.SerializerMethodField()

    class Meta:
        model = Order
        fields = "__all__"

    def get_car_name(self, obj):
        if obj.car:
            return f"{obj.car.brand} {obj.car.model} ({obj.car.year})"
        return None

    def get_delivery_city_name(self, obj):
        return obj.delivery_city.name if obj.delivery_city else None

    def get_delivery_address_text(self, obj):
        return obj.delivery_address.address_line if obj.delivery_address else None

    def get_import_status(self, obj):
        import_info = getattr(obj.car, "import_info", None)
        return import_info.status if import_info else None

    def get_car_main_image(self, obj):
        request = self.context.get("request")

        if obj.car and obj.car.main_image:
            image_url = obj.car.main_image.url

            if request:
                return request.build_absolute_uri(image_url)

            return image_url

        return None