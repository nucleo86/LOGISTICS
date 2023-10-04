from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('work_shift/<int:event_id>/<int:employee_id>/', views.work_shift, name='work_shift'),
    path('get_first_employee_for_event/<int:event_id>/', views.get_first_employee_for_event, name='get_first_employee_for_event'),
    path('api/work_shifts/', views.get_work_shifts, name='get_work_shifts'),
    path('test/', views.test_view, name='test_view'),
]

