from django.contrib import admin

from policy_areas.models import PolicyArea


@admin.register(PolicyArea)
class PolicyAreaAdmin(admin.ModelAdmin):
    pass
