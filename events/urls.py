from django.urls import path
from . import views

app_name = 'events'

urlpatterns = [
    path('', views.event_list, name='event_list'),
    path('<int:event_id>/', views.event_detail, name='event_detail'),
    path('employee/<int:pk>/', views.employee_detail, name='employee_detail'),
    path('work_shift/', views.work_shift, name='work_shift'),
]

