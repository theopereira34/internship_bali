# Generated by Django 5.0.6 on 2024-08-02 02:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('APM_APP', '0027_remove_farmerschedule_activity_data_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='farmerschedule',
            name='activity_description',
            field=models.TextField(default='No description available'),
        ),
        migrations.AddField(
            model_name='farmerschedule',
            name='activity_duration',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='farmerschedule',
            name='activity_name',
            field=models.CharField(default='Unknown Activity', max_length=100),
        ),
        migrations.AddField(
            model_name='farmerschedule',
            name='activity_start_after_hours',
            field=models.IntegerField(default=0),
        ),
    ]
