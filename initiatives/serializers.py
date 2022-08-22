import enum
from typing import Any, Iterable, OrderedDict

from backend.serializers import SlugRelatedOptionalField, convert_var_to_obj
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

    better_regulation_requirement = SlugRelatedOptionalField(
        queryset=BetterRegulationRequirement.objects.all(),
        many=True,
        read_only=False,
        slug_field="name",
    )
    committee = SlugRelatedOptionalField(
        queryset=Committee.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    expert_group = SlugRelatedOptionalField(
        queryset=ExpertGroup.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    initiative_category = SlugRelatedOptionalField(
        queryset=Category.objects.all(),
        many=True,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    legal_basis = LegalBasisSerializer(many=True, read_only=False)
    policy_areas = PolicyAreaSerializer(many=True, read_only=False)
    publications = serializers.ReadOnlyField()
    foreseen_act_type = SlugRelatedOptionalField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    unit = SlugRelatedOptionalField(
        queryset=Unit.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    topics = TopicSerializer(many=True, read_only=False)
    stage = serializers.SlugRelatedField(
        queryset=Stage.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
    )
    initiative_status = SlugRelatedOptionalField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    receiving_feedback_status = SlugRelatedOptionalField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    publications = PublicationSerializer(many=True, read_only=False, required=False)

    class Meta:
        model = Initiative
        fields = "__all__"

    def handle_validated_data(self, validated_data: dict) -> dict:
        foreseen_act_type = convert_var_to_obj(
            validated_data.pop("foreseen_act_type"), Type, "code"
        )
        stage = convert_var_to_obj(validated_data.pop("stage"), Stage, "code")
        expert_group = convert_var_to_obj(
            validated_data.pop("expert_group"), ExpertGroup, "name"
        )
        committee = convert_var_to_obj(
            validated_data.pop("committee"), Committee, "name"
        )
        initiative_category = convert_var_to_obj(
            validated_data.pop("initiative_category"), Category, "name"
        )
        better_regulation_requirement = convert_var_to_obj(
            validated_data.pop("better_regulation_requirement"),
            BetterRegulationRequirement,
            "name",
        )
        legal_basis = convert_var_to_obj(
            validated_data.pop("legal_basis"), LegalBasis, "name"
        )
        policy_areas = convert_var_to_obj(
            validated_data.pop("policy_areas"), PolicyArea, "code"
        )
        topics = convert_var_to_obj(validated_data.pop("topics"), Topic, "code")
        unit = convert_var_to_obj(validated_data.pop("unit"), Unit, "name")
        initiative_status = convert_var_to_obj(
            validated_data.pop("initiative_status"), Status, "name"
        )
        receiving_feedback_status = convert_var_to_obj(
            validated_data.pop("receiving_feedback_status"), Status, "name"
        )

        return {
            "foreseen_act_type": foreseen_act_type,
            "stage": stage,
            "expert_group": expert_group,
            "committee": committee,
            "initiative_category": initiative_category,
            "better_regulation_requirement": better_regulation_requirement,
            "legal_basis": legal_basis,
            "policy_areas": policy_areas,
            "topics": topics,
            "unit": unit,
            "initiative_status": initiative_status,
            "receiving_feedback_status": receiving_feedback_status,
            "validated_data": validated_data,
        }

    def add_many_to_many_relations(self, fields: dict, instance: Initiative) -> None:
        if isinstance(fields["initiative_category"], Iterable):
            for ic in fields["initiative_category"]:
                instance.initiative_category.add(ic)
        if isinstance(fields["expert_group"], Iterable):
            for eg in fields["expert_group"]:
                instance.expert_group.add(eg)
        if isinstance(fields["better_regulation_requirement"], Iterable):
            for brr in fields["better_regulation_requirement"]:
                instance.better_regulation_requirement.add(brr)
        if isinstance(fields["legal_basis"], Iterable):
            for lb in fields["legal_basis"]:
                instance.legal_basis.add(lb)
        if isinstance(fields["policy_areas"], Iterable):
            for pa in fields["policy_areas"]:
                instance.policy_areas.add(pa)
        if isinstance(fields["topics"], Iterable):
            for t in fields["topics"]:
                instance.topics.add(t)

    def create(self, validated_data):
        data = self.handle_validated_data(validated_data)

        validated_data = data.pop("validated_data")
        publications = validated_data.pop("publications")

        initiative = Initiative.objects.create(
            foreseen_act_type=data["foreseen_act_type"],
            stage=data["stage"],
            committee=data["committee"],
            unit=data["unit"],
            initiative_status=data["initiative_status"],
            receiving_feedback_status=data["receiving_feedback_status"],
            **data["validated_data"],
        )
        self.add_many_to_many_relations(data, initiative)
        for publication in publications:
            publication = PublicationSerializer(data=publication)
            publication = publication.save()
            initiative.publications.addd(publication)
        initiative.save()
        return initiative

    def update(self, instance, validated_data):
        # convert slugrelated fields to objects
        data = self.handle_validated_data(validated_data)

        validated_data = data.pop("validated_data")
        publications = validated_data.pop("publications")
        reference = validated_data.pop("reference")
        initiative, _ = Initiative.objects.update_or_create(
            reference=reference,
            defaults={
                "foreseen_act_type": data["foreseen_act_type"],
                "stage": data["stage"],
                "committee": data["committee"],
                "unit": data["unit"],
                "initiative_status": data["initiative_status"],
                "receiving_feedback_status": data["receiving_feedback_status"]
                ** validated_data,
            },
        )
        # add slugrelatedfield to instance
        self.add_many_to_many_relations(data, initiative)

        initiative.save()
        return initiative
