from django.shortcuts import render

from rest_framework import viewsets,generics
from rest_framework.permissions import AllowAny,IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework import status


from .models import User
from .serializers import UserSerializes,RegisterSerializer,ChangePasswordSerializer,ForgotPasswordSerializer,ResetPasswordSerializer

from core.permissions import IsAdminUserRole

from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.conf import settings
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django_countries import countries

from .emails import send_activation_email
from .tokens import account_activation_token

from django.shortcuts import redirect
from django.conf import settings
# Create your views here.


class UserViewsets(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=UserSerializes
    permission_classes=[IsAdminUserRole]
    
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        send_activation_email(user, self.request)

class ProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializes
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

    def patch(self, request, *args, **kwargs):
        print("PATCH DATA:", request.data)
        serializer = self.get_serializer(
            self.get_object(),
            data=request.data,
            partial=True
        )

        if not serializer.is_valid():
            print("SERIALIZER ERRORS:", serializer.errors)
            return Response(serializer.errors, status=400)

        serializer.save()
        return Response(serializer.data)
    

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
    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "L'adresse email est obligatoire."},
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.filter(email=email).first()

        if not user:
            return Response(
                {"error": "Aucun utilisateur n'existe avec cette adresse email."},
                status=status.HTTP_404_NOT_FOUND
            )

        # Ici ton code existant pour générer le token et envoyer l'email

        return Response(
            {"message": "Un lien de réinitialisation a été envoyé à votre adresse email."},
            status=status.HTTP_200_OK
        )


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


class CountryListView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        data = [
            {"code": code, "name": name}
            for code, name in countries
        ]
        return Response(data)



class ActivateAccountView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

        except Exception:
            return redirect(
                f"{settings.FRONTEND_URL}/login?activation=failed"
            )

        if (
            user is not None
            and account_activation_token.check_token(user, token)
        ):
            user.is_active = True
            user.is_verified = True
            user.save()

            return redirect(
                f"{settings.FRONTEND_URL}/login?activated=true"
            )

        return redirect(
            f"{settings.FRONTEND_URL}/login?activation=failed"
        )
        
        
class ResendActivationEmailView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")

        if not email:
            return Response(
                {"error": "Email requis."},
                status=400
            )

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "Aucun compte trouvé avec cet email."},
                status=404
            )

        if user.is_active:
            return Response(
                {"message": "Ce compte est déjà activé."},
                status=200
            )

        send_activation_email(user, request)

        return Response({
            "message": "Un nouvel email d’activation a été envoyé."
        })