from django.contrib import admin

from .models import Committee, ExpertGroup


@admin.register(ExpertGroup)
class ExpertGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    pass
