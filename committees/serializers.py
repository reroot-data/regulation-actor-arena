from rest_framework import serializers

from .models import Committee, ExpertGroup, Unit, UserType, WorkGroup


class WorkGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkGroup
        fields = "__all__"


class UserTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserType
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
