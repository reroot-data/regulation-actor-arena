from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from sentiments.models import Sentiment
from sentiments.serializers import SentimentSerializer

from .models import Attachment, AttachmentType, Link, Publication
from .serializers import (
    AttachmentSerializer,
    AttachmentTypeSerializer,
    LinkSerializer,
    PublicationSentimentsSerializer,
    PublicationSerializer,
)


class LinkViewSet(viewsets.ModelViewSet):
    queryset = Link.objects.all()
    serializer_class = LinkSerializer


class AttachmentViewSet(viewsets.ModelViewSet):
    queryset = Attachment.objects.all()
    serializer_class = AttachmentSerializer


class AttachmentTypeViewSet(viewsets.ModelViewSet):
    queryset = AttachmentType.objects.all()
    serializer_class = AttachmentTypeSerializer


class PublicationViewSet(viewsets.ModelViewSet):
    queryset = Publication.objects.all()
    serializer_class = PublicationSerializer

    @action(detail=True, methods=["get"])
    def sentiments(self, request, pk=None):
        publication = self.get_object()
        serializer = PublicationSentimentsSerializer(publication, many=False)
        return Response(serializer.data)
