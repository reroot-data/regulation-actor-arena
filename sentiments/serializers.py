from rest_framework import serializers

from .models import Sentiment


class SentimentSerializer(serializers.ModelSerializer):

    organization = serializers.ReadOnlyField(
        source="feedback.organization", label="organization"
    )
    text = serializers.ReadOnlyField(source="feedback.feedback_en", label="feedback")

    class Meta:
        model = Sentiment
        fields = "__all__"
