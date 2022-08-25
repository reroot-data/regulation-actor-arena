from django.contrib import admin

from feedbacks.models import Feedback, FeedbackAttachment


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    search_fields = ("id",)


@admin.register(FeedbackAttachment)
class FeedbackAttachmentAdmin(admin.ModelAdmin):
    pass
