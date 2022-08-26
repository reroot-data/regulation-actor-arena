from django.shortcuts import render
from feedbacks.models import Feedback
from publication_documents.models import Publication
from rest_framework import viewsets

from .models import Sentiment
from .serializers import SentimentSerializer


class SentimentViewSet(viewsets.ModelViewSet):
    queryset = Sentiment.objects.all()
    serializer_class = SentimentSerializer
