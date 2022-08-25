from backend.serializers import SlugRelatedGetOrCreateField
from committees.models import UserType
from countries.models import Country
from rest_framework import serializers

from initiatives.models import Status

from .models import Feedback, FeedbackAttachment


class FeedbackSerializer(serializers.ModelSerializer):
    country = SlugRelatedGetOrCreateField(
        queryset=Country.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    user_type = SlugRelatedGetOrCreateField(
        queryset=UserType.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    class Meta:
        model = Feedback
        fields = "__all__"


class FeedbackAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = FeedbackAttachment
        fields = "__all__"