from django.contrib import admin

from feedbacks.models import Feedback, FeedbackAttachment


class FeedbackInline(admin.StackedInline):
    model = Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = (
        "id",
        "publication",
    )


@admin.register(FeedbackAttachment)
class FeedbackAttachmentAdmin(admin.ModelAdmin):
    pass
