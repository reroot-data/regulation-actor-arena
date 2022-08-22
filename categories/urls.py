from django.urls import include, path
from rest_framework import routers

from .views import BetterRegulationRequirementViewSet, CategoryViewSet

router = routers.DefaultRouter()
router.register(r"better_regulation_requirements", BetterRegulationRequirementViewSet)
router.register(r"categories", CategoryViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
