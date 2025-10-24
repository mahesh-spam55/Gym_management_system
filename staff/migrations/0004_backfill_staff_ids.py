from django.db import migrations
from django.db.models import Q
import re


def backfill_staff_ids(apps, schema_editor):
    Staff = apps.get_model('staff', 'Staff')
    prefix = 'STF'
    width = 4
    pat = re.compile(rf'^{prefix}(\d+)$')

    def next_id():
        max_n = 0
        for cid in Staff.objects.exclude(Q(staff_id__isnull=True) | Q(staff_id='')) \
                                 .values_list('staff_id', flat=True):
            m = pat.match(cid)
            if m:
                try:
                    n = int(m.group(1))
                    if n > max_n:
                        max_n = n
                except ValueError:
                    pass
        return f"{prefix}{str(max_n + 1).zfill(width)}"

    qs = Staff.objects.filter(Q(staff_id__isnull=True) | Q(staff_id=''))
    for s in qs.order_by('id'):
        s.staff_id = next_id()
        s.save(update_fields=['staff_id'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0003_alter_staff_staff_id_staff_unique_staff_id_when_set'),
    ]

    operations = [
        migrations.RunPython(backfill_staff_ids, noop),
    ]
