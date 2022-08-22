from django.shortcuts import render
from rest_framework import viewsets

from .models import Initiative, LegalBasis, Stage, Status, Type
from .serializers import (
    InitiativeSerializer,
    LegalBasisSerializer,
    StageSerializer,
    StatusSerializer,
    TypeSerializer,
)


class LegalBasisViewSet(viewsets.ModelViewSet):
    queryset = LegalBasis.objects.all()
    serializer_class = LegalBasisSerializer


class StatusViewSet(viewsets.ModelViewSet):
    queryset = Status.objects.all()
    serializer_class = StatusSerializer


class StageViewSet(viewsets.ModelViewSet):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer


class TypeViewSet(viewsets.ModelViewSet):
    queryset = Type.objects.all()
    serializer_class = TypeSerializer


class InitiativeViewSet(viewsets.ModelViewSet):
    queryset = Initiative.objects.all()
    serializer_class = InitiativeSerializer
