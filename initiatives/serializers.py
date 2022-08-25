import enum
from typing import Any, Iterable, OrderedDict

from backend.serializers import (
    SlugRelatedGetOrCreateField,
    SlugRelatedOptionalField,
    convert_var_to_obj,
)
from categories.models import BetterRegulationRequirement, Category
from committees.models import Committee, ExpertGroup, Unit
from policy_areas.models import PolicyArea
from policy_areas.serializers import PolicyAreaSerializer
from publication_documents.models import Attachment, Publication
from publication_documents.serializers import PublicationSerializer
from rest_framework import serializers
from topics.models import Topic
from topics.serializer import TopicSerializer

from .models import Initiative, LegalBasis, Stage, Status, Type


class StatusSerializer(serializers.ModelSerializer):
    class meta:
        model = Status
        fields = "__all__"


class LegalBasisSerializer(serializers.ModelSerializer):
    class Meta:
        model = LegalBasis
        fields = "__all__"


class StageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stage
        fields = "__all__"


class TypeSerializer(serializers.ModelSerializer):
    class meta:
        model = Type
        fields = "__all__"


class InitiativeSerializer(serializers.ModelSerializer):

    better_regulation_requirement = SlugRelatedGetOrCreateField(
        queryset=BetterRegulationRequirement.objects.all(),
        many=True,
        read_only=False,
        slug_field="name",
    )
    committee = SlugRelatedGetOrCreateField(
        queryset=Committee.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    expert_group = SlugRelatedGetOrCreateField(
        queryset=ExpertGroup.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    initiative_category = SlugRelatedGetOrCreateField(
        queryset=Category.objects.all(),
        many=True,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    legal_basis = LegalBasisSerializer(many=True, read_only=True)
    policy_areas = PolicyAreaSerializer(many=True, read_only=True)
    publications = PublicationSerializer(many=True, read_only=True)
    foreseen_act_type = SlugRelatedGetOrCreateField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    unit = SlugRelatedGetOrCreateField(
        queryset=Unit.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    topics = TopicSerializer(many=True, read_only=True)
    stage = SlugRelatedGetOrCreateField(
        queryset=Stage.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
    )
    initiative_status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    receiving_feedback_status = SlugRelatedGetOrCreateField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )

    class Meta:
        model = Initiative
        fields = "__all__"
