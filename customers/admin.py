from django.contrib import admin
from .models import Member


@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ("member_id", "name", "contact")
    search_fields = ("member_id", "name", "contact")
