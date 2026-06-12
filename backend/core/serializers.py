from rest_framework import serializers 
from .models import OriginCountry,MalaisianCity,Notification, AuditLog

class OriginCountrySerializers(serializers.ModelSerializer):
    class Meta:
        model=OriginCountry
        fields = ("id", "country", "country_name", "is_active", "created_at")

class MalaisianCitySerializers(serializers.ModelSerializer):
    class Meta:
        model=MalaisianCity
        fields="__all__"
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model=Notification
        fields="__all__"
        

class AuditLogSerializer(serializers.ModelSerializer):
    user_email = serializers.SerializerMethodField()

    class Meta:
        model = AuditLog
        fields = (
            "id",
            "user",
            "user_email",
            "action",
            "message",
            "created_at",
        )

    def get_user_email(self, obj):
        return obj.user.email if obj.user else None