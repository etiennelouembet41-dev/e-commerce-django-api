from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Address
from .serializers import AddressSerializer
# Create your views here.

class AddressViewsets(viewsets.ModelViewSet):
    serializer_class=AddressSerializer
    permission_classes=[IsAuthenticated]
    
    def get_queryset(self):
        
        queryset = Address.objects.select_related(
            "user",
            "city"
        )
        
        if self.request.user.role == "admin":
            return Address.objects.all()
        
        return Address.objects.filter(user=self.request.user)#retourne unique les addresses des utilisateurs connectés très important 
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)#pour que l'addresse crée soit enregistrée à l'utilisateur connecté et non un autre utilisateur 
        
