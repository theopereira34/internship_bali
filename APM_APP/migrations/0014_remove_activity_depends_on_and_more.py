# Generated by Django 5.0.6 on 2024-07-31 03:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0013_remove_activity_dependencies_activity_depends_on'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='depends_on',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='parallel_start_delay',
        ),
    ]
