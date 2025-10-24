from django.db import models
from django.db.models import Q
import re


class Staff(models.Model):
    staff_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=50)
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["position", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["staff_id"],
                name="unique_staff_id_when_set",
                condition=Q(staff_id__isnull=False) & ~Q(staff_id=""),
            )
        ]

    def __str__(self) -> str:
        return f"{self.staff_id} - {self.name}" if self.staff_id else self.name

    @staticmethod
    def _next_sequential_id(prefix: str = "STF", width: int = 4) -> str:
        candidates = (
            Staff.objects.filter(staff_id__startswith=prefix)
            .exclude(staff_id="")
            .exclude(staff_id__isnull=True)
            .values_list("staff_id", flat=True)
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
        if not self.staff_id:
            self.staff_id = self._next_sequential_id()
        super().save(*args, **kwargs)
