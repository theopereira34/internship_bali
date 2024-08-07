from django import forms
from django.contrib.auth.forms import UserChangeForm, PasswordResetForm, UserCreationForm
from .models import User, Crop, Equipment, Material, ActivityCategory, Activity, FarmerAgriculturalWork


class UserUpdateForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    def __init__(self, *args, **kwargs):
        fields_to_display = kwargs.pop('fields_to_display', None)
        super(UserUpdateForm, self).__init__(*args, **kwargs)
        if fields_to_display:
            for field_name in set(self.fields) - set(fields_to_display):
                self.fields.pop(field_name)

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2', 'user_type']
        widgets = {
            'user_type': forms.Select(choices=User.USER_TYPES),
        }

class CropForm(forms.ModelForm):
    class Meta:
        model = Crop
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'same-width'}),
            'description': forms.TextInput(attrs={'class': 'same-width'}),
        }

class EquipmentForm(forms.ModelForm):
    class Meta:
        model = Equipment
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'same-width'}),
            'description': forms.TextInput(attrs={'class': 'same-width'}),
        }

class MaterialForm(forms.ModelForm):
    class Meta:
        model = Material
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'same-width'}),
            'description': forms.TextInput(attrs={'class': 'same-width'}),
        }

class ActivityCategoryForm(forms.ModelForm):
    class Meta:
        model = ActivityCategory
        fields = ['name', 'description']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'same-width'}),
            'description': forms.TextInput(attrs={'class': 'same-width'}),
        }

class ActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = ['name', 'description', 'crop', 'category', 'equipment', 'materials', 'duration', 'depends_on', 'start_after_hours', 'optionnal']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'same-width'}),
            'description': forms.TextInput(attrs={'class': 'same-width'}),
            'equipment': forms.CheckboxSelectMultiple(),
            'materials': forms.CheckboxSelectMultiple(),
            'depends_on': forms.Select(),
            'start_after_hours': forms.NumberInput(),
            'optionnal': forms.CheckboxInput()
        }

    def __init__(self, *args, **kwargs):
        self.instance = kwargs.get('instance', None)
        super(ActivityForm, self).__init__(*args, **kwargs)

class FarmerAgriculturalWorkForm(forms.ModelForm):
    optional_activities = forms.ModelMultipleChoiceField(
        queryset=Activity.objects.filter(optionnal=True),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )

    class Meta:
        model = FarmerAgriculturalWork
        fields = ['crop', 'land_size', 'start_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

    def __init__(self, *args, **kwargs):
        super(FarmerAgriculturalWorkForm, self).__init__(*args, **kwargs)
        for activity in Activity.objects.filter(optionnal=True):
            self.fields[f'optional_activity_start_{activity.id}'] = forms.DateTimeField(
                required=False,
                widget=forms.DateTimeInput(attrs={'type': 'datetime-local'}),
                label=f'Start date for {activity.name}'
            )