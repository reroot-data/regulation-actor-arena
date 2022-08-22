from django.shortcuts import render
from rest_framework import viewsets

from .models import Committee, ExpertGroup, TargetGroup, Unit, WorkGroup
from .serializers import (
    CommitteeSerializer,
    ExpertGroupSerializer,
    TargetGroupSerializer,
    UnitSerializer,
    WorkGroupSerializer,
)


class ExpertGroupViewSet(viewsets.ModelViewSet):
    queryset = ExpertGroup.objects.all()
    serializer_class = ExpertGroupSerializer


class TargetGroupViewSet(viewsets.ModelViewSet):
    queryset = TargetGroup.objects.all()
    serializer_class = TargetGroupSerializer


class WorkGroupViewSet(viewsets.ModelViewSet):
    queryset = WorkGroup.objects.all()
    serializer_class = WorkGroupSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class CommitteeViewSet(viewsets.ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
