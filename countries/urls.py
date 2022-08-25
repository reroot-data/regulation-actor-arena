from django.urls import include, path
from rest_framework import routers

from .views import CountryViewSet

router = routers.DefaultRouter()
router.register(r"countries", CountryViewSet)

urlpatterns = [path("", include(router.urls))]
