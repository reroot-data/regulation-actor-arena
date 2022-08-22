from django.urls import include, path
from rest_framework import routers

from .views import (
    CommitteeViewSet,
    ExpertGroupViewSet,
    TargetGroupViewSet,
    UnitViewSet,
    WorkGroupViewSet,
)

router = routers.DefaultRouter()
router.register(r"units", UnitViewSet)
router.register(r"work_groups", WorkGroupViewSet)
router.register(r"target_groups", TargetGroupViewSet)
router.register(r"expert_groups", ExpertGroupViewSet)
router.register(r"committees", CommitteeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
