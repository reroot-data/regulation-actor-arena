from typing import Sequence

from django.contrib import admin

from .models import Sentiment


@admin.register(Sentiment)
class SentimentAdmin(admin.ModelAdmin):
    readonly_fields: Sequence[str] = ("feedback",)
