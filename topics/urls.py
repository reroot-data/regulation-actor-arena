from django.urls import include, path
from rest_framework import routers

from .views import TopicViewSet

router = routers.DefaultRouter()
router.register(r"topics", TopicViewSet)

urlpatterns = [
    path("", include(router.urls)),
]
