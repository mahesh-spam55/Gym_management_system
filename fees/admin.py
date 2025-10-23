from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ("member", "amount", "transaction_type", "paid_on")
    list_filter = ("transaction_type", "paid_on")
    search_fields = ("member__name", "member__member_id")
