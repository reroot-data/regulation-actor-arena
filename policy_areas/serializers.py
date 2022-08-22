from rest_framework import serializers

from .models import PolicyArea


class PolicyAreaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PolicyArea
        fields = "__all__"
