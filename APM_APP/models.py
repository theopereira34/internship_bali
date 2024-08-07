from datetime import timedelta
from django.db import models
from django.contrib.auth.models import AbstractUser
from collections import defaultdict

class User(AbstractUser):
    USER_TYPES = (
        ('farmer', 'Farmer'),
        ('village_admin', 'Village Admin'),
        ('system_admin', 'System Admin'),
    )
    user_type = models.CharField(max_length=15, choices=USER_TYPES, default='farmer')

    def __str__(self):
        return self.username

class Crop(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Equipment(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class ActivityCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Activity(models.Model):
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    duration = models.IntegerField()
    equipment = models.ManyToManyField(Equipment)
    materials = models.ManyToManyField(Material)
    optionnal = models.BooleanField(default=False)
    depends_on = models.ForeignKey('self', null=True, blank=True, on_delete=models.SET_NULL, related_name='dependent_activities')
    start_after_hours = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class FarmerAgriculturalWork(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    land_size = models.FloatField()
    start_date = models.DateTimeField()
    estimated_harvest_date = models.DateTimeField(null=True, blank=True)
    estimated_harvest_quantity = models.FloatField(null=True, blank=True)

    def calculate_estimates(self, optional_activities=None, optional_activities_dates=None):
        # Supprimer les anciens enregistrements de FarmerSchedule
        FarmerSchedule.objects.filter(farmer_work=self).delete()

        current_date = self.start_date
        activities = list(Activity.objects.filter(crop=self.crop, optionnal=False).order_by('id'))

        if optional_activities:
            activities.extend(optional_activities)

        activity_end_dates = defaultdict(lambda: self.start_date)
        last_end_date = self.start_date

        for activity in activities:
            if activity.depends_on:
                dependency_end_date = activity_end_dates[activity.depends_on.id]
                start_date = dependency_end_date + timedelta(hours=activity.start_after_hours)
            else:
                start_date = self.start_date + timedelta(hours=activity.start_after_hours)

            if optional_activities_dates and activity.id in optional_activities_dates:
                start_date = optional_activities_dates[activity.id]

            end_date = start_date + timedelta(hours=activity.duration)

            activity_end_dates[activity.id] = end_date

            FarmerSchedule.objects.create(
                farmer_work=self,
                activity=activity,
                scheduled_date=start_date,
                end_date=end_date,
                human_resources_needed=0,
                funds_needed=0.0,
                activity_name=activity.name,
                activity_description=activity.description,
                activity_duration=activity.duration,
                activity_start_after_hours=activity.start_after_hours
            )

            if activity.depends_on is None or activity.start_after_hours > 0:
                current_date = max(current_date, end_date)

            last_end_date = max(last_end_date, end_date)

        self.estimated_harvest_date = last_end_date
        self.estimated_harvest_quantity = self.land_size * 1500  # Remplacer par la logique réelle de calcul
        self.save()


class FarmerSchedule(models.Model):
    farmer_work = models.ForeignKey(FarmerAgriculturalWork, on_delete=models.CASCADE)
    activity = models.ForeignKey(Activity, on_delete=models.CASCADE)
    scheduled_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    human_resources_needed = models.IntegerField()
    funds_needed = models.FloatField()
    # New fields to store activity details at the time of schedule creation
    activity_name = models.CharField(max_length=100, default='Unknown Activity')
    activity_description = models.TextField(default='No description available')
    activity_duration = models.IntegerField(default=0)
    activity_start_after_hours = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if not self.id:
            self.activity_name = self.activity.name
            self.activity_description = self.activity.description
            self.activity_duration = self.activity.duration
            self.activity_start_after_hours = self.activity.start_after_hours
        super(FarmerSchedule, self).save(*args, **kwargs)



class FarmerActivityEquipment(models.Model):
    schedule = models.ForeignKey(FarmerSchedule, on_delete=models.CASCADE)
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    quantity_needed = models.IntegerField()

class FarmerActivityMaterial(models.Model):
    schedule = models.ForeignKey(FarmerSchedule, on_delete=models.CASCADE)
    material = models.ForeignKey(Material, on_delete=models.CASCADE)
    quantity_needed = models.IntegerField()

class HarvestStatistics(models.Model):
    date = models.DateField()
    activity_category = models.ForeignKey(ActivityCategory, on_delete=models.CASCADE)
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    quantity = models.FloatField()
    num_farmers = models.IntegerField()
