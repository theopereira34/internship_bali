from django.urls import path
from . import views



urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile, name='profile'),
    path('reset_password/', views.reset_password, name='reset_password'),
    path('change_password/', views.CustomPasswordChangeView.as_view(), name='change_password'),
    path('', views.home, name='home'),

    path('management/', views.ManagementView.as_view(), name='management'),
    path('activities/', views.ActivityListView.as_view(), name='activity_list'),
    #path('get_existing_steps/<int:crop_id>/', views.get_existing_steps, name='get_existing_steps'),
    path('activities/update/<int:pk>/', views.ActivityUpdateView.as_view(), name='activity_update'),
    path('activities/delete/<int:pk>/', views.ActivityDeleteView.as_view(), name='activity_delete'),
    path('generate-schedule/', views.GenerateScheduleView.as_view(), name='generate_schedule'),
    path('schedule-list/', views.ScheduleListView.as_view(), name='schedule_list'),
    path('schedule/update/<int:pk>/', views.UpdateScheduleView.as_view(), name='update_schedule'),
    path('schedule/delete/<int:pk>/', views.DeleteScheduleView.as_view(), name='delete_schedule'),
    path('calendar/<int:pk>/', views.CalendarDetailView.as_view(), name='calendar_detail'),

    # ... autres urls ...

]
