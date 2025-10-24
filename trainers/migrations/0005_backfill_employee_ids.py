from django.db import migrations
from django.db.models import Q
import re


def backfill_employee_ids(apps, schema_editor):
    Trainer = apps.get_model('trainers', 'Trainer')
    prefix = 'TRN'
    width = 4
    pat = re.compile(rf'^{prefix}(\d+)$')

    def next_id():
        max_n = 0
        for cid in Trainer.objects.exclude(Q(employee_id__isnull=True) | Q(employee_id=''))\
                                   .values_list('employee_id', flat=True):
            m = pat.match(cid)
            if m:
                try:
                    n = int(m.group(1))
                    if n > max_n:
                        max_n = n
                except ValueError:
                    pass
        return f"{prefix}{str(max_n + 1).zfill(width)}"

    qs = Trainer.objects.filter(Q(employee_id__isnull=True) | Q(employee_id=''))
    for t in qs.order_by('id'):
        t.employee_id = next_id()
        t.save(update_fields=['employee_id'])


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0004_alter_trainer_employee_id_and_more'),
    ]

    operations = [
        migrations.RunPython(backfill_employee_ids, noop),
    ]
