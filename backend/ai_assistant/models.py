from django.db import models
from django.conf import settings
from cars.models import Car
# Create your models here.


class  AIQuestion(models.Model):
    user=models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_questions"
    )
    
    question=models.TextField()
    answer=models.TextField()

    recommended_cars=models.ManyToManyField(
        Car,
        blank=True,
        related_name="ai_recommendations"
    )
    
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.question[:80]