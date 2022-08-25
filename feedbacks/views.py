from django.shortcuts import render
from rest_framework import viewsets

from .models import Feedback, FeedbackAttachment
from .serializers import FeedbackAttachmentSerializer, FeedbackSerializer


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class FeedbackAttachmentViewSet(viewsets.ModelViewSet):
    queryset = FeedbackAttachment.objects.all()
    serializer_class = FeedbackAttachmentSerializer
