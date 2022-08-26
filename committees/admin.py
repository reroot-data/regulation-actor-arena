from django.contrib import admin

from .models import Committee, ExpertGroup, Unit, UserType, WorkGroup


@admin.register(UserType)
class UserTypeAdmin(admin.ModelAdmin):
    pass


@admin.register(WorkGroup)
class WorkGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(ExpertGroup)
class ExpertGroupAdmin(admin.ModelAdmin):
    pass


@admin.register(Unit)
class UnitAdmin(admin.ModelAdmin):
    pass


@admin.register(Committee)
class CommitteeAdmin(admin.ModelAdmin):
    pass
