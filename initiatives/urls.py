from django.urls import include, path
from rest_framework import routers

from .views import (
    InitiativeViewSet,
    LegalBasisViewSet,
    StageViewSet,
    StatusViewSet,
    TypeViewSet,
)

router = routers.DefaultRouter()
router.register(r"legal_basisses/", LegalBasisViewSet)
router.register(r"stages", StageViewSet)
router.register(r"initiatives", InitiativeViewSet)
router.register(r"types", TypeViewSet)
router.register(r"statusses", StatusViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
