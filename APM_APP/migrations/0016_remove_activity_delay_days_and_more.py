# Generated by Django 5.0.6 on 2024-07-31 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0015_remove_activity_step_activity_delay_days_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='delay_days',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='reference_activity',
        ),
        migrations.RemoveField(
            model_name='activity',
            name='start_type',
        ),
        migrations.AddField(
            model_name='activity',
            name='step',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
    ]
