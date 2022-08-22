from django.urls import include, path
from rest_framework import routers

from .views import PolicyAreaViewSet

router = routers.DefaultRouter()
router.register(r"policy_areas", PolicyAreaViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
