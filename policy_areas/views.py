from rest_framework import viewsets

from policy_areas.models import PolicyArea
from policy_areas.serializers import PolicyAreaSerializer


class PolicyAreaViewSet(viewsets.ModelViewSet):
    queryset = PolicyArea.objects.all()
    serializer_class = PolicyAreaSerializer
