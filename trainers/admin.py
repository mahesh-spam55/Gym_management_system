from django.contrib import admin
from .models import Trainer


@admin.register(Trainer)
class TrainerAdmin(admin.ModelAdmin):
    list_display = ("employee_id", "first_name", "last_name", "date_of_joining")
    search_fields = ("employee_id", "first_name", "last_name")
    list_filter = ("date_of_joining",)
