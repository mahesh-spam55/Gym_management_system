from django.db import models


class Staff(models.Model):
    staff_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50)

    class Meta:
        ordering = ["name"]

    def __str__(self) -> str:
        return f"{self.staff_id} - {self.name}" if self.staff_id else self.name
