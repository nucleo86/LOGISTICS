from django.contrib import admin
from .models import Employee, Client, Event, Assignment, Place

admin.site.register(Employee)
admin.site.register(Client)
admin.site.register(Event)
admin.site.register(Assignment)
admin.site.register(Place)
