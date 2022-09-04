from django.shortcuts import render
from feedbacks.models import Feedback, FeedbackAttachment
from feedbacks.serializers import FeedbackAttachmentSerializer, FeedbackSerializer
from rest_framework import viewsets


class FeedbackViewSet(viewsets.ModelViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer
