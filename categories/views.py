from django.shortcuts import render
from rest_framework import viewsets

from .models import BetterRegulationRequirement, Category
from .serializers import BetterRegulationRequirementSerializer, CategorySerializer


class BetterRegulationRequirementViewSet(viewsets.ModelViewSet):
    queryset = BetterRegulationRequirement.objects.all()
    serializer_class = BetterRegulationRequirementSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
