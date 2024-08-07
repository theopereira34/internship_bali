from collections import defaultdict
from datetime import timedelta
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import JsonResponse
from django.urls import reverse_lazy
from .forms import CustomUserCreationForm, FarmerAgriculturalWorkForm, UserUpdateForm, CropForm, EquipmentForm, MaterialForm, ActivityCategoryForm, ActivityForm
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views import View
from .models import Crop, Equipment, FarmerAgriculturalWork, FarmerSchedule, Material, ActivityCategory, Activity
from django.views.generic.edit import UpdateView, DeleteView
from io import BytesIO
import base64
import matplotlib.pyplot as plt # type: ignore
import matplotlib.dates as mdates # type: ignore


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'register.html', {'form': form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                return redirect('home')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    messages.success(request, 'You have successfully logged out.')
    return redirect('home')

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=request.user, fields_to_display=['username', 'email'])
        if form.is_valid():
            form.save()
            messages.success(request, 'Your profile was successfully updated!')
            return redirect('profile')
    else:
        form = UserUpdateForm(instance=request.user, fields_to_display=['username', 'email', 'first_name', 'last_name'])
    return render(request, 'profile.html', {'form': form})

def reset_password(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST) # type: ignore
        if form.is_valid():
            form.save()
            messages.success(request, 'Password reset link has been sent to your email.')
            return redirect('login')
    else:
        form = PasswordResetForm() # type: ignore
    return render(request, 'reset_password.html', {'form': form})

class CustomPasswordChangeView(PasswordChangeView):
    template_name = 'change_password.html'
    success_url = reverse_lazy('profile')

    def form_valid(self, form):
        messages.success(self.request, 'Your password was successfully updated!')
        return super().form_valid(form)

def home(request):
    return render(request, 'home.html')

class SystemAdminRequiredMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.is_authenticated and self.request.user.user_type == 'system_admin'

class ManagementView(View):
    def get(self, request):
        forms = {
            'crop_form': CropForm(),
            'equipment_form': EquipmentForm(),
            'material_form': MaterialForm(),
            'activity_category_form': ActivityCategoryForm(),
            'activity_form': ActivityForm(),
        }

        context = {
            'crops': Crop.objects.all(),
            'equipments': Equipment.objects.all(),
            'materials': Material.objects.all(),
            'activity_categories': ActivityCategory.objects.all(),
            'activities': Activity.objects.all(),
        }

        context.update(forms)

        return render(request, 'management.html', context)

    def post(self, request):
        forms = {
            'crop_submit': CropForm(request.POST),
            'equipment_submit': EquipmentForm(request.POST),
            'material_submit': MaterialForm(request.POST),
            'activity_category_submit': ActivityCategoryForm(request.POST),
            'activity_submit': ActivityForm(request.POST),
        }

        for key, form in forms.items():
            if key in request.POST and form.is_valid():
                form.save()
                return redirect('activity_list')

        delete_actions = {
            'delete_crop': Crop,
            'delete_equipment': Equipment,
            'delete_material': Material,
            'delete_activity_category': ActivityCategory,
            'delete_activity': Activity,
        }

        for action, model in delete_actions.items():
            if action in request.POST:
                instance = get_object_or_404(model, pk=request.POST.get(action))
                instance.delete()
                return redirect('management')

        return self.get(request)

class ActivityListView(View):
    def get(self, request):
        crops = Crop.objects.all()
        activities = Activity.objects.select_related('crop', 'category').prefetch_related('equipment', 'materials')
        return render(request, 'activity_list.html', {'crops': crops, 'activities': activities})

class ActivityUpdateView(View):
    def get(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        form = ActivityForm(instance=activity)
        return render(request, 'activity_update.html', {'form': form})

    def post(self, request, pk):
        activity = get_object_or_404(Activity, pk=pk)
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('activity_list')
        return render(request, 'activity_update.html', {'form': form})

class ActivityDeleteView(DeleteView):
    model = Activity
    template_name = 'activity_confirm_delete.html'
    success_url = reverse_lazy('activity_list')

class GenerateScheduleView(View):
    def get(self, request):
        form = FarmerAgriculturalWorkForm()
        return render(request, 'generate_schedule.html', {'form': form})

    def post(self, request):
        form = FarmerAgriculturalWorkForm(request.POST)
        if form.is_valid():
            calendar = form.save(commit=False)
            calendar.user = request.user
            calendar.save()

            optional_activities = form.cleaned_data['optional_activities']
            calendar.calculate_estimates(optional_activities)
            
            return redirect('schedule_list')
        return render(request, 'generate_schedule.html', {'form': form})

class ScheduleListView(View):
    def get(self, request):
        calendars = FarmerAgriculturalWork.objects.all()
        return render(request, 'schedule_list.html', {'calendars': calendars})

class UpdateScheduleView(View):
    def get(self, request, pk):
        schedule = get_object_or_404(FarmerAgriculturalWork, pk=pk)
        form = FarmerAgriculturalWorkForm(instance=schedule)
        return render(request, 'update_schedule.html', {'form': form})

    def post(self, request, pk):
        schedule = get_object_or_404(FarmerAgriculturalWork, pk=pk)
        form = FarmerAgriculturalWorkForm(request.POST, instance=schedule)
        if form.is_valid():
            schedule = form.save(commit=False)
            optional_activities = form.cleaned_data.get('optional_activities')
            optional_activities_dates = {
                activity.id: form.cleaned_data[f'optional_activity_start_{activity.id}']
                for activity in optional_activities
                if form.cleaned_data[f'optional_activity_start_{activity.id}']
            }
            schedule.calculate_estimates(optional_activities, optional_activities_dates)
            schedule.save()
            return redirect('schedule_list')
        return render(request, 'update_schedule.html', {'form': form})

class DeleteScheduleView(View):
    def post(self, request, pk):
        schedule = get_object_or_404(FarmerAgriculturalWork, pk=pk)
        schedule.delete()
        return redirect('schedule_list')

class CalendarDetailView(View):
    def get(self, request, pk):
        calendar = get_object_or_404(FarmerAgriculturalWork, pk=pk)
        scheduled_activities = FarmerSchedule.objects.filter(farmer_work=calendar)

        fig, ax = plt.subplots(figsize=(10, 6))

        for scheduled_activity in scheduled_activities:
            start_date = mdates.date2num(scheduled_activity.scheduled_date)
            end_date = mdates.date2num(scheduled_activity.end_date)
            duration = end_date - start_date
            ax.barh(scheduled_activity.activity_name, duration, left=start_date, color='skyblue', height=0.9)

        ax.set_xlabel('Date and Time')
        ax.set_ylabel('Activity')
        ax.xaxis_date()
        ax.xaxis.set_major_locator(mdates.HourLocator(interval=30))
        ax.xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d %I:%M %p'))
        plt.xticks(rotation=75)
        plt.tight_layout()

        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        image_png = buffer.getvalue()
        buffer.close()

        graphic = base64.b64encode(image_png).decode('utf-8')

        return render(request, 'calendar_detail.html', {
            'calendar': calendar,
            'scheduled_activities': scheduled_activities,
            'graphic': graphic,
        })


