from backend.serializers import SlugRelatedGetOrCreateField
from committees.models import UserType
from countries.models import Country
from feedbacks.models import Feedback
from initiatives.models import Status
from rest_framework import serializers


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
