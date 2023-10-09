from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('employee_availability_table/', views.employee_availability_table, name='employee_availability_table'),
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('work_shift/<int:event_id>/<int:employee_id>/', views.work_shift, name='work_shift'),
    path('get_first_employee_for_event/<int:event_id>/', views.get_first_employee_for_event, name='get_first_employee_for_event'),
    path('api/work_shifts/', views.get_work_shifts, name='get_work_shifts'),
    path('get_event_date_range/<int:event_id>/', views.get_event_date_range, name='get_event_date_range'),
    path('employee_availability/', views.employee_availability, name='employee_availability'),
]

