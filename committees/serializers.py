from rest_framework import serializers

from .models import Committee, ExpertGroup, TargetGroup, Unit, WorkGroup


class WorkGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkGroup
        fields = "__all__"


class TargetGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetGroup
        fields = "__all__"


class ExpertGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpertGroup
        fields = "__all__"


class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Unit
        fields = "__all__"


class CommitteeSerializer(serializers.ModelSerializer):
    class meta:
        model = Committee
        fields = "__all__"
