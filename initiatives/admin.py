from django.contrib import admin

from .models import Initiative, LegalBasis, Stage, Type


@admin.register(LegalBasis)
class LegalBasisAdmin(admin.ModelAdmin):
    pass


@admin.register(Type)
class TypeAdmin(admin.ModelAdmin):
    pass


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    pass


@admin.register(Initiative)
class InitiativeAdmin(admin.ModelAdmin):
    search_fields = ("id",)
