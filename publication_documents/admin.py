from django.contrib import admin
from feedbacks.admin import FeedbackInline
from initiatives.models import Initiative

from .models import Attachment, Publication


class PublicationInline(admin.StackedInline):
    model = Initiative.publications.through
    extra = 0


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    inlines = (FeedbackInline,)
    list_display = ("id", "title", "total_feedback")
    search_fields = ("id",)

    def has_change_permission(self, request, obj=None):
        return False
