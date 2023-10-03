from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('work_shifts/<int:employee_id>/', views.work_shift_list, name='work_shift_list'),
    path('add_work_shift/', views.add_work_shift, name='add_work_shift'),
]

