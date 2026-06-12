from django.urls import path
from .views import DashboardStatsView
from .bi_views import BusinessIntelligenceView

urlpatterns = [
    path("stats/", DashboardStatsView.as_view()),
    path("business-intelligence/", BusinessIntelligenceView.as_view()),
]
