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
        
    
    
class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model=User
        fields=(
           
            "id",
            "email",
            "username",
            "first_name",
            "last_name",
            "phone_number",
            "password",
            
        )
        
    def create(self, validated_data):
        password=validated_data.pop("password")
        user=User(**validated_data)
        user.set_password(password)
        user.save()
        return user
    