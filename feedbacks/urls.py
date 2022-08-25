from django.urls import include, path
from rest_framework import routers

from .views import FeedbackAttachmentViewSet, FeedbackViewSet

router = routers.DefaultRouter()
router.register(r"feedbacks", FeedbackViewSet)
router.register(r"feedback_attachments", FeedbackAttachmentViewSet)

urlpatterns = [path("", include(router.urls))]
