from datetime import date
from django.db import models


class Payment(models.Model):
    class TransactionType(models.TextChoices):
        CASH = "cash", "Cash"
        UPI = "upi", "UPI"
        CARD = "card", "Card"
        OTHER = "other", "Other"

    class MembershipType(models.TextChoices):
        THREE = "3", "3 months"
        SIX = "6", "6 months"
        NINE = "9", "9 months"
        TWELVE = "12", "1 year"

    member = models.ForeignKey("customers.Member", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    paid_on = models.DateField(default=date.today)
    membership_type = models.CharField(max_length=2, choices=MembershipType.choices, default=MembershipType.THREE)

    class Meta:
        ordering = ["-paid_on", "-id"]

    def __str__(self) -> str:
        return f"{self.member} - {self.amount} on {self.paid_on}"
