from django.db.models.signals import post_save
from django.dispatch import receiver
from feedbacks.models import Feedback
from sentiments.models import Sentiment
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer


@receiver(post_save, sender=Feedback)
def feedback_add_sentiment(sender, instance, *args, **kwargs):

    if not instance.feedback_en:
        return

    if instance.user_type:
        if not instance.user_type.include_in_sentiment_analysis:
            return

    sid_obj = SentimentIntensityAnalyzer()
    sentiment_dict = sid_obj.polarity_scores(instance.feedback_en)

    if sentiment_dict:
        sentiment, created = Sentiment.objects.update_or_create(
            feedback=instance,
            defaults={
                "positive": sentiment_dict["pos"],
                "neutral": sentiment_dict["neu"],
                "negative": sentiment_dict["neg"],
                "compound": sentiment_dict["compound"],
            },
        )

        # Update publication sentiment plot
        instance.publication_object.save()
