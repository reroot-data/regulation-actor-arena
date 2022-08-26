from lib2to3.pytree import Base
from typing import Any, Optional

from committees.models import UserType
from django.core.management.base import BaseCommand, CommandParser

from ...models import Feedback


class Command(BaseCommand):
    help = "fetch sentiments for all feedbacks that have english feedback"

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        feedbacks = Feedback.objects.filter(
            feedback_en__isnull=False, organization__isnull=False
        )
        feedback_count = feedbacks.count()
        for i, feedback in enumerate(feedbacks):
            print(f"feedback {i+1} of {feedback_count} ")
            feedback.save()
