from rest_framework import viewsets

from topics.models import Topic
from topics.serializer import TopicSerializer


class TopicViewSet(viewsets.ModelViewSet):
    queryset = Topic.objects.all()
    serializer_class = TopicSerializer
