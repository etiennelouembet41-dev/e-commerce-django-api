from django.shortcuts import render
from rest_framework import viewsets
from .models import User
from .serializers import UserSerializes
# Create your views here.


class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializes