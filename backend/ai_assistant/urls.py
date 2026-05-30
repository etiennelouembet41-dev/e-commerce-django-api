from django.urls import path
from .views import GeminiCarAssistantView

urlpatterns = [
    path("chat/", GeminiCarAssistantView.as_view()),
]
