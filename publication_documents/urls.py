from django.urls import include, path
from rest_framework import routers

from .views import (
    AttachmentTypeViewSet,
    AttachmentViewSet,
    LinkViewSet,
    PublicationViewSet,
)

router = routers.DefaultRouter()
router.register(r"links", LinkViewSet)
router.register(r"attachment_types", AttachmentTypeViewSet)
router.register(r"attachments", AttachmentViewSet)
router.register(r"publications", PublicationViewSet)

urlpatterns = [path("", include(router.urls))]
