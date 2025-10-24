from django.db import migrations


def overwrite_employee_ids(apps, schema_editor):
    Trainer = apps.get_model('trainers', 'Trainer')
    prefix = 'TRN'
    width = 4
    counter = 1
    for t in Trainer.objects.order_by('id'):
        t.employee_id = f"{prefix}{str(counter).zfill(width)}"
        t.save(update_fields=['employee_id'])
        counter += 1


def noop(apps, schema_editor):
    pass


class Migration(migrations.Migration):

    dependencies = [
        ('trainers', '0005_backfill_employee_ids'),
    ]

    operations = [
        migrations.RunPython(overwrite_employee_ids, noop),
    ]
