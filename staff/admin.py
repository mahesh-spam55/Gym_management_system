from django.contrib import admin

from .models import Staff


@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ("staff_id", "name", "role", "contact")
    search_fields = ("staff_id", "name", "role")
