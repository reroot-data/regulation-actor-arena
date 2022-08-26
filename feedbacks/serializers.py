from backend.serializers import SlugRelatedGetOrCreateField
from committees.models import UserType
from countries.models import Country
from initiatives.models import Status
from rest_framework import serializers
from sentiments.serializers import SentimentSerializer

from .models import Feedback, FeedbackAttachment


class FeedbackSentimentSerializer(serializers.ModelSerializer):
    sentiments = SentimentSerializer(many=True, read_only=True)

    class Meta:
        model = Feedback
        fields = ["organization", "feedback_en", "sentiments"]


class FeedbackSerializer(serializers.ModelSerializer):
    country = SlugRelatedGetOrCreateField(
        queryset=Country.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
        required=False,
    )
    status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    user_type = serializers.SlugRelatedField(
        queryset=UserType.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
        required=False,
    )

    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackAttachment
        fields = "__all__"
