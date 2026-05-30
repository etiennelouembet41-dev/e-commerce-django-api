from django.shortcuts import render

from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny,IsAuthenticated

from .models import User
from .serializers import UserSerializes,RegisterSerializer

from core.permissions import IsAdminUserRole

# Create your views here.


class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializes
    permission_classes=[IsAdminUserRole]
    
class RegisterView(generics.CreateAPIView):
    serializer_class=RegisterSerializer
    permission_classes=[AllowAny]

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class=UserSerializes
    permission_classes=[IsAuthenticated]
    
    def get_object(self):
        return self.request.user
    
    