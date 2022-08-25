from django.urls import include, path
from rest_framework import routers

from .views import (
    CommitteeViewSet,
    ExpertGroupViewSet,
    UnitViewSet,
    UserTypeViewSet,
    WorkGroupViewSet,
)

router = routers.DefaultRouter()
router.register(r"units", UnitViewSet)
router.register(r"work_groups", WorkGroupViewSet)
router.register(r"expert_groups", ExpertGroupViewSet)
router.register(r"user_types", UserTypeViewSet)
router.register(r"committees", CommitteeViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
