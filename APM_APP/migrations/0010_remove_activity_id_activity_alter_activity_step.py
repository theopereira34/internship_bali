# Generated by Django 5.0.6 on 2024-07-26 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0009_farmerschedule_end_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='ID_Activity',
        ),
        migrations.AlterField(
            model_name='activity',
            name='step',
            field=models.PositiveIntegerField(),
        ),
    ]
