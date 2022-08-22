from lib2to3.pytree import convert
from sre_parse import State

from backend.serializers import SlugRelatedOptionalField, convert_var_to_obj
from categories.models import Category
from committees.models import TargetGroup, WorkGroup
from initiatives.models import Stage, Status, Type
from rest_framework import serializers

from .models import Attachment, AttachmentType, Link, Publication


class LinkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Link
        fields = "__all__"


class AttachmentSerializer(serializers.ModelSerializer):
    type = SlugRelatedOptionalField(
        queryset=AttachmentType.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    work_type = SlugRelatedOptionalField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    category = SlugRelatedOptionalField(
        queryset=Category.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    work_group = SlugRelatedOptionalField(
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
    class AttachmentType:
        model = AttachmentType
        fields = "__all__"


class PublicationSerializer(serializers.ModelSerializer):
    type = SlugRelatedOptionalField(
        queryset=Type.objects.all(),
        many=False,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    attachment = AttachmentSerializer(many=True, read_only=False)
    stage = SlugRelatedOptionalField(
        queryset=Stage.objects.all(),
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
    target_groups = SlugRelatedOptionalField(
        queryset=TargetGroup.objects.all(),
        many=True,
        read_only=False,
        slug_field="name",
        allow_null=True,
    )
    front_end_stage = SlugRelatedOptionalField(
        queryset=Stage.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )
    useful_links = LinkSerializer(many=True, read_only=False)
    initiative_status = SlugRelatedOptionalField(
        queryset=Status.objects.all(),
        many=False,
        read_only=False,
        slug_field="code",
        allow_null=True,
    )

    class meta:
        model = Publication
        fields = "__all__"

    def handle_validated_data(self, validated_data: dict) -> dict:
        type = convert_var_to_obj(validated_data.pop("type"), Type, "code")
        stage = convert_var_to_obj(validated_data.pop("stage"), Stage, "code")
        receiving_feedback_status = convert_var_to_obj(
            validated_data["receiving_feedback_status"], Status, "name"
        )
        target_groups = convert_var_to_obj(
            validated_data.pop("target_groups"), TargetGroup, "name"
        )
        front_end_stage = convert_var_to_obj(
            validated_data.pop("front_end_stage"), Stage, "code"
        )
        initiative_status = convert_var_to_obj(
            validated_data.pop("initiative_status"), Status, "code"
        )

        return {
            "type": type,
            "stage": stage,
            "receiving_feedback_status": receiving_feedback_status,
            "target_groups": target_groups,
            "front_end_stage": front_end_stage,
            "initiative_status": initiative_status,
            "validated_data": validated_data,
        }

    def create(self, validated_data):
        data = self.handle_validated_data(validated_data)
        useful_links = data.pop("useful_links")
        attachments = data.pop("attachments")

        publication = Publication.objects.create(
            type=type,
            stage=data["stage"],
            receiving_feedback_status=data["receiving_feedback_status"],
            target_groups=data["target_groups"],
            front_end_stage=data["front_end_stage"],
            initiative_status=data["initiative_status"],
            **data["validated_data"]
        )

        for link in useful_links:
            link, _ = Link.objects.create(**link)
            publication.useful_links.add(link)

        for attachment in attachments:
            attachment = AttachmentSerializer(data=attachment)
            attachment = attachment.save()
            publication.useful_links.add(attachment)

        publication.save()
        return publication
