from django.db import models
from django.db.models import Q
import re

# Create your models here.

class Member(models.Model):
    member_id = models.CharField(max_length=20, null=True, blank=True)
    name = models.CharField(max_length=150)
    contact = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    date_of_joining = models.DateField(null=True, blank=True)
    membership_due_date = models.DateField(null=True, blank=True)
    position = models.PositiveIntegerField(default=0, db_index=True)

    class Meta:
        ordering = ["position", "name"]
        constraints = [
            models.UniqueConstraint(
                fields=["member_id"],
                name="unique_member_id_when_set",
                condition=Q(member_id__isnull=False) & ~Q(member_id=""),
            )
        ]

    def __str__(self) -> str:
        return f"{self.member_id} - {self.name}" if self.member_id else self.name

    @staticmethod
    def _next_sequential_id(prefix: str = "MEM", width: int = 4) -> str:
        candidates = (
            Member.objects.filter(member_id__startswith=prefix)
            .exclude(member_id="")
            .exclude(member_id__isnull=True)
            .values_list("member_id", flat=True)
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
        if not self.member_id:
            self.member_id = self._next_sequential_id()
        super().save(*args, **kwargs)
