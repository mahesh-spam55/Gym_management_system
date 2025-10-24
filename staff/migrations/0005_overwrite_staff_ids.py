from django.db import migrations


def overwrite_staff_ids(apps, schema_editor):
    Staff = apps.get_model('staff', 'Staff')
    prefix = 'STF'
    width = 4
    counter = 1
    for s in Staff.objects.order_by('id'):
        s.staff_id = f"{prefix}{str(counter).zfill(width)}"
        s.save(update_fields=['staff_id'])
        counter += 1


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('staff', '0004_backfill_staff_ids'),
    ]

    operations = [
        migrations.RunPython(overwrite_staff_ids, noop),
    ]
