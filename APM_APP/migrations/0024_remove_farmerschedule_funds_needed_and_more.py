# Generated by Django 5.0.6 on 2024-08-02 02:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0023_remove_farmeragriculturalwork_has_unplanned_event_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='farmerschedule',
            name='funds_needed',
        ),
        migrations.RemoveField(
            model_name='farmerschedule',
            name='human_resources_needed',
        ),
        migrations.AddField(
            model_name='farmerschedule',
            name='activity_data',
            field=models.JSONField(default=0),
            preserve_default=False,
        ),
    ]
