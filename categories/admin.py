from django.contrib import admin

from categories.models import BetterRegulationRequirement, Category


@admin.register(BetterRegulationRequirement)
class BetterRegulationRequirementAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass
