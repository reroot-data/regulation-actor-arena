from django.shortcuts import render
from rest_framework import viewsets

from .models import Attachment, AttachmentType, Link, Publication
from .serializers import (
    AttachmentSerializer,
    AttachmentTypeSerializer,
    LinkSerializer,
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
