from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Document
from .serializers import DocumentSerializer

from django.utils import timezone
from rest_framework.decorators import action
from rest_framework.response import Response

from core.models import Notification


class DocumentViewSet(viewsets.ModelViewSet):

    serializer_class = DocumentSerializer
    permission_classes = [IsAuthenticated]

    
    
    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):

        document = self.get_object()

        document.status = "approved"
        document.validated_by = request.user
        document.validated_at = timezone.now()
        document.save()

        Notification.objects.create(
            user=document.order.user,
            title="Document validé",
            message=f"Votre document {document.get_document_type_display()} a été validé."
        )

        return Response({"message": "Document validé"})
    
    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):

        document = self.get_object()

        reason = request.data.get("reason", "")

        document.status = "rejected"
        document.rejection_reason = reason
        document.validated_by = request.user
        document.validated_at = timezone.now()
        document.save()

        Notification.objects.create(
            user=document.order.user,
            title="Document rejeté",
            message=f"Document rejeté : {reason}"
        )

        return Response({"message": "Document rejeté"})
    
    def get_queryset(self):
        return Document.objects.filter(
            order__user=self.request.user
        )