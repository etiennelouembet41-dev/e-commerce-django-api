from django.shortcuts import render

from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response


from .models import User
from .serializers import UserSerializes,RegisterSerializer,ChangePasswordSerializer,ForgotPasswordSerializer,ResetPasswordSerializer

from core.permissions import IsAdminUserRole

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

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
    

class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = request.user

        if not user.check_password(serializer.validated_data["old_password"]):
            return Response(
                {"error": "Ancien mot de passe incorrect"},
                status=400
            )

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"message": "Mot de passe modifié avec succès"})



#mail oublié
User = get_user_model()


class ForgotPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ForgotPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data["email"]
        user = User.objects.filter(email=email).first()

        if user:
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            reset_link = f"http://localhost:5173/reset-password?uid={uid}&token={token}"

            send_mail(
                "Réinitialisation de votre mot de passe",
                f"Bonjour,\n\nCliquez sur ce lien pour réinitialiser votre mot de passe :\n{reset_link}",
                settings.DEFAULT_FROM_EMAIL,
                [user.email],
                fail_silently=False,
            )

        return Response({
            "message": "Si cet email existe, un lien de réinitialisation a été envoyé."
        })


class ResetPasswordView(APIView):
    permission_classes = []

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            uid = force_str(urlsafe_base64_decode(serializer.validated_data["uid"]))
            user = User.objects.get(pk=uid)
        except Exception:
            return Response({"error": "Lien invalide"}, status=400)

        token = serializer.validated_data["token"]

        if not default_token_generator.check_token(user, token):
            return Response({"error": "Token invalide ou expiré"}, status=400)

        user.set_password(serializer.validated_data["new_password"])
        user.save()

        return Response({"message": "Mot de passe réinitialisé avec succès"})

