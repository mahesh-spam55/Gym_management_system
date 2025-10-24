from django.db import models
from django.db.models import Q
import re


class Trainer(models.Model):
    employee_id = models.CharField(max_length=20, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, blank=True)
    address = models.TextField(blank=True)
    contact = models.CharField(max_length=20, blank=True)
    specialization = models.CharField(max_length=100, blank=True)
    date_of_joining = models.DateField()
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["position", "first_name", "last_name"]
        constraints = [
            models.UniqueConstraint(
                fields=["employee_id"],
                name="unique_trainer_employee_id_when_set",
                condition=Q(employee_id__isnull=False) & ~Q(employee_id=""),
            )
        ]

    def __str__(self) -> str:
        name = f"{self.first_name} {self.last_name}".strip()
        return f"{self.employee_id} - {name}" if self.employee_id else name

    @staticmethod
    def _next_sequential_id(prefix: str = "TRN", width: int = 4) -> str:
        candidates = (
            Trainer.objects.filter(employee_id__startswith=prefix)
            .exclude(employee_id="")
            .exclude(employee_id__isnull=True)
            .values_list("employee_id", flat=True)
        )
        max_n = 0
        pattern = re.compile(rf"^{prefix}(\d+)$")
        for cid in candidates:
            m = pattern.match(cid)
            if m:
                try:
                    n = int(m.group(1))
                    if n > max_n:
                        max_n = n
                except ValueError:
                    continue
        return f"{prefix}{str(max_n + 1).zfill(width)}"

    def save(self, *args, **kwargs):
        if not self.employee_id:
            self.employee_id = self._next_sequential_id()
        super().save(*args, **kwargs)
