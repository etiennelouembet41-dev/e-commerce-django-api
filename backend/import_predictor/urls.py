from django.urls import path
from .views import ImportCostPredictionView

urlpatterns = [
    path("predict/", ImportCostPredictionView.as_view()),
]