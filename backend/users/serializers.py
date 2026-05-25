from rest_framework import serializers 
from .models import User

class UserSerializes(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=(
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "profile_image",
            "country",
            "city",
            "role",
            "gender",
            "is_verified",
            "created_at",
            
            
            
        )
        
        read_on_fields=("id", "role", "is_verified", "created_at",)