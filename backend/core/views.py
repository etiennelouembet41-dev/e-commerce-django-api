from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import OriginCountry,MalaisianCity,Notification
from .serializers import OriginCountrySerializers,MalaisianCitySerializers,NotificationSerializer
# Create your views here.

class OriginCountryViewsets(viewsets.ModelViewSet):
    queryset=OriginCountry.objects.all()
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
