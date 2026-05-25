from rest_framework import serializers
from .models import ImportInfo

class ImportInfoSerializers(serializers.ModelSerializer):
    class Meta:
        model=ImportInfo
        fields="__all__"

        