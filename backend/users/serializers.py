from rest_framework import serializers 
from .models import User

from django_countries.serializer_fields import CountryField

class UserSerializes(serializers.ModelSerializer):

    nationality = CountryField(name_only=False)

    class Meta:
        model = User
        fields = (
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
            "nationality",
            "is_verified",
            "created_at",
            "is_staff",
            "is_superuser",
        )

        read_only_fields = (
            "id",
            "email",
            "role",
            "is_verified",
            "created_at",
            "is_staff",
            "is_superuser",
        )
        
    
    
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
            "gender",
            "nationality",
            
        )
    
    def validate_nationality(self, value):
        if not value:
            raise serializers.ValidationError(
                "La nationalité est obligatoire."
            )
        return value
        
    def create(self, validated_data):
        password=validated_data.pop("password")
        user=User(**validated_data)
        user.set_password(password)
        user.is_active = False
        user.is_verified = False
        user.save()
        return user

from django.contrib.auth.password_validation import validate_password

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(write_only=True)
    new_password = serializers.CharField(write_only=True, min_length=8)

    def validate_new_password(self, value):
        validate_password(value)
        return value

class ForgotPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()


class ResetPasswordSerializer(serializers.Serializer):
    uid = serializers.CharField()
    token = serializers.CharField()
    new_password = serializers.CharField(write_only=True, min_length=8)