from rest_framework import serializers 
from .models import Address

class AddressSerializers(serializers.ModelSerializer):
    class Meta:
        model=Address
        fields="__all__"
        read_on_fields=("user",)