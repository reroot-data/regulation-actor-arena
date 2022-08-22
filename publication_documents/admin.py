from django.contrib import admin

from .models import Attachment, Publication


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    pass


@admin.register(Publication)
class PublicationAdmin(admin.ModelAdmin):
    pass
