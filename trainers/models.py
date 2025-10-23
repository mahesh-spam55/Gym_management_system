from django.db import models


class Trainer(models.Model):
    employee_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    date_of_joining = models.DateField()

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return f"{self.employee_id} - {name}" if self.employee_id else name
