from django.contrib import admin

from feedbacks.models import Feedback, FeedbackAttachment


class FeedbackInline(admin.StackedInline):
    model = Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ("id", "publication", "organization")
    list_filter = ("user_type",)
    list_display = (
        "id",
        "organization",
    )

    def has_change_permission(self, request, obj=None):
        return False


@admin.register(FeedbackAttachment)
class FeedbackAttachmentAdmin(admin.ModelAdmin):
    pass
