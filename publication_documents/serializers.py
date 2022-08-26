from lib2to3.pytree import convert
from sre_parse import State

from backend.serializers import (
    SlugRelatedGetOrCreateField,
    SlugRelatedOptionalField,
    convert_var_to_obj,
)
from categories.models import Category
from committees.models import WorkGroup
from feedbacks.serializers import FeedbackSentimentSerializer
from initiatives.models import Stage, Status, Type
from rest_framework import serializers

from .models import Attachment, AttachmentType, Link, Publication


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
    type = SlugRelatedGetOrCreateField(
        queryset=AttachmentType.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    work_type = SlugRelatedGetOrCreateField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    category = SlugRelatedGetOrCreateField(
        queryset=Category.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    work_group = SlugRelatedGetOrCreateField(
        queryset=WorkGroup.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Attachment
        fields = "__all__"


class AttachmentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AttachmentType
        fields = "__all__"


class PublicationSentimentsSerializer(serializers.ModelSerializer):
    feedbacks = FeedbackSentimentSerializer(many=True, read_only=True)

    class Meta:
        model = Publication
        fields = ("title", "feedbacks")


class PublicationSerializer(serializers.ModelSerializer):
    type = SlugRelatedGetOrCreateField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    stage = SlugRelatedGetOrCreateField(
        queryset=Stage.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    receiving_feedback_status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )

    front_end_stage = SlugRelatedGetOrCreateField(
        queryset=Stage.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    attachment = AttachmentSerializer(many=True, read_only=True)
    useful_links = LinkSerializer(many=True, read_only=True)
    initiative_status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Publication
        fields = "__all__"
