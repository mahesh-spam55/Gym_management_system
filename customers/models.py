from django.db import models

# Create your models here.

class Member(models.Model):
    member_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    membership_due_date = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.member_id} - {self.name}" if self.member_id else self.name
