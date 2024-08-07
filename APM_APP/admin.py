from django.contrib import admin
from .models import User, Crop, Equipment, Material, ActivityCategory, Activity, FarmerAgriculturalWork, FarmerSchedule, FarmerActivityEquipment, FarmerActivityMaterial, HarvestStatistics

admin.site.register(User)
admin.site.register(Crop)
admin.site.register(Equipment)
admin.site.register(Material)
admin.site.register(ActivityCategory)
admin.site.register(Activity)
admin.site.register(FarmerAgriculturalWork)
admin.site.register(FarmerSchedule)
admin.site.register(FarmerActivityEquipment)
admin.site.register(FarmerActivityMaterial)
admin.site.register(HarvestStatistics)
