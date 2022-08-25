from django.shortcuts import render
from rest_framework import viewsets

from .models import Committee, ExpertGroup, Unit, UserType, WorkGroup
from .serializers import (
    CommitteeSerializer,
    ExpertGroupSerializer,
    UnitSerializer,
    UserTypeSerializer,
    WorkGroupSerializer,
)


class ExpertGroupViewSet(viewsets.ModelViewSet):
    queryset = ExpertGroup.objects.all()
    serializer_class = ExpertGroupSerializer


class UserTypeViewSet(viewsets.ModelViewSet):
    queryset = UserType.objects.all()
    serializer_class = UserTypeSerializer


class WorkGroupViewSet(viewsets.ModelViewSet):
    queryset = WorkGroup.objects.all()
    serializer_class = WorkGroupSerializer


class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer


class CommitteeViewSet(viewsets.ModelViewSet):
    queryset = Committee.objects.all()
    serializer_class = CommitteeSerializer
