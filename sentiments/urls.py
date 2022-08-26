from django.urls import include, path
from rest_framework import routers

from .views import SentimentViewSet

router = routers.DefaultRouter()
router.register(r"sentiments", SentimentViewSet)

urlpatterns = [path("", include(router.urls))]
