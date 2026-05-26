from django.urls import path
from .views import ImportTrackingView

urlpatterns = [
    path("tracking/<int:order_id>/", ImportTrackingView.as_view()),
]
