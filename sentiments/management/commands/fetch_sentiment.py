from typing import Any, Optional

from django.core.management.base import BaseCommand, CommandParser
from feedbacks.models import Feedback
from sentiments.models import Sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


class Command(BaseCommand):
    help = "Fetch sentiment of a certain feedback"

    def add_arguments(self, parser: CommandParser) -> None:
        parser.add_argument("feedback_id", type=int)

    def handle(self, *args: Any, **options: Any) -> Optional[str]:
        feedback = Feedback.objects.get(id=options["feedback_id"])

        sid_obj = SentimentIntensityAnalyzer()
        sentiment_dict = sid_obj.polarity_scores(feedback.feedback_en)
        print(sentiment_dict)

        if sentiment_dict:
            sentiment, created = Sentiment.objects.update_or_create(
                feedback=feedback,
                defaults={
                    "positive": sentiment_dict["pos"],
                    "neutral": sentiment_dict["neu"],
                    "negative": sentiment_dict["neg"],
                    "compound": sentiment_dict["compound"],
                },
            )
