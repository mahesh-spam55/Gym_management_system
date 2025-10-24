from datetime import date
from django.db import models


class Payment(models.Model):
    class TransactionType(models.TextChoices):
        CASH = "cash", "Cash"
        UPI = "upi", "UPI"
        CARD = "card", "Card"
        OTHER = "other", "Other"

    class MembershipType(models.TextChoices):
        ONE = "1", "1 month"
        TWO = "2", "2 months"
        THREE = "3", "3 months"
        FOUR = "4", "4 months"
        FIVE = "5", "5 months"
        SIX = "6", "6 months"
        EIGHT = "8", "8 months"
        TEN = "10", "10 months"
        TWELVE = "12", "12 months"

    member = models.ForeignKey("customers.Member", on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TransactionType.choices)
    paid_on = models.DateField(default=date.today)
    membership_type = models.CharField(max_length=2, choices=MembershipType.choices, default=MembershipType.THREE)

    class Meta:
        ordering = ["-paid_on", "-id"]

    def __str__(self) -> str:
        return f"{self.member} - {self.amount} on {self.paid_on}"

