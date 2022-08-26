from django.shortcuts import render
from feedbacks.models import Feedback
from publication_documents.models import Publication
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Sentiment
from .serializers import SentimentSerializer


class SentimentViewSet(viewsets.ModelViewSet):
    queryset = Sentiment.objects.all()
    serializer_class = SentimentSerializer

    @action(detail=True, methods=["get"])
    def publication(self, request, pk=None):
        publication = Publication.objects.get(pk=pk)
        queryset = Sentiment.objects.filter(feedback__publication_object__pk=pk)
        serializer = SentimentSerializer(queryset, many=True)
        response_data = {"title": publication.title, "sentiments": serializer.data}
        return Response(response_data)
