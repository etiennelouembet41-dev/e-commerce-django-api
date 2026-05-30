from django.contrib import admin
from .models import AIQuestion
# Register your models here.

@admin.register
class AIQuestionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "question", "created_at")
    search_fields = ("question", "answer", "user__email")
    list_filter = ("created_at",)