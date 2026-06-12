from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from core.realtime import send_realtime_notification
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from .models import OriginCountry,MalaisianCity,Notification,AuditLog
from .serializers import OriginCountrySerializers,MalaisianCitySerializers,NotificationSerializer,AuditLogSerializer
from core.activity import create_audit_log
# Create your views here.

class OriginCountryViewsets(viewsets.ModelViewSet):
    queryset = OriginCountry.objects.filter(is_active=True).order_by("country")
    serializer_class=OriginCountrySerializers
    
class MalaisianCityViewsets(viewsets.ModelViewSet):
    queryset=MalaisianCity.objects.all()
    serializer_class=MalaisianCitySerializers
    
class NotificationViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class=NotificationSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        return Notification.objects.filter(
            user=self.request.user
        )

    @action(detail=True, methods=["post"], url_path="mark-as-read")
    def mark_as_read(self, request, pk=None):
        notification = self.get_object()
        notification.is_read = True
        notification.save()
        return Response({
            "message": "Notification marked as read"
        })

class AuditLogViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = AuditLog.objects.select_related("user").all()
    serializer_class = AuditLogSerializer
    permission_classes = [IsAdminUser]
