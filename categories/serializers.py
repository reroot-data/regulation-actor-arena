from rest_framework import serializers

from .models import BetterRegulationRequirement, Category


class BetterRegulationRequirementSerializer(serializers.ModelSerializer):
    class Meta:
        model = BetterRegulationRequirement
        fields = "__all__"


class CategorySerializer(serializers.ModelSerializer):
    class meta:
        model = Category
        fields = "__all__"
