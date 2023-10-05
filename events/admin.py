from django.contrib import admin
from .models import Employee, Client, Event, Assignment, Place, WorkShift, EmployeeSpecialization, Department, Specialization, Group

admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Assignment)
admin.site.register(Place)
admin.site.register(WorkShift)
admin.site.register(EmployeeSpecialization)
admin.site.register(Department)
admin.site.register(Specialization)
admin.site.register(Group)
