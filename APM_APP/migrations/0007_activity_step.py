# Generated by Django 5.0.6 on 2024-07-16 06:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0006_activity_id_activity_alter_activity_duration'),
    ]

    operations = [
        migrations.AddField(
            model_name='activity',
            name='step',
            field=models.IntegerField(default=0),
        ),
    ]
