# Generated by Django 5.0.6 on 2024-08-02 02:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0024_remove_farmerschedule_funds_needed_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='farmerschedule',
            name='end_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='farmerschedule',
            name='scheduled_date',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
