from django.db import models

class Employee(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    specialization = models.CharField(max_length=100, null=True, blank=True)
    e_mail = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Client(models.Model):
    name = models.CharField(max_length=255)
    e_mail = models.CharField(max_length=255, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField(null=True, blank=True)
    e_mail = models.CharField(max_length=255, null=True, blank=True)

    def __str__(self):
        return self.name

class Event(models.Model):
    name = models.CharField(max_length=255, null=True)
    start_time = models.DateField()
    end_time = models.DateField(null=True, blank=True)
    protocol_number = models.CharField(max_length=100, blank=True)
    place = models.ForeignKey(Place, on_delete=models.SET_NULL, null=True, blank=True)
    clients = models.ManyToManyField(Client, blank=True)
    project_managers = models.ManyToManyField(Employee, related_name='managed_events', blank=True)
    seller = models.ForeignKey(Employee, related_name='sold_events_for', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        start_date_str = format(self.start_time, '%d.%m.%Y') if self.start_time else ''
        end_date_str = format(self.end_time, '%d.%m.%Y') if self.end_time else ''
        return f"{self.protocol_number} {self.name or ''} {start_date_str} {end_date_str}"

class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} assigned to {self.event}"

class WorkShift(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    work_date = models.DateField()
    start_time = models.TimeField()
    hours = models.IntegerField()

    def clean(self):
        # Tutaj można dodać logikę sprawdzania kolizji
        pass

    def save(self, *args, **kwargs):
        self.clean()
        super(WorkShift, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.employee} - {self.event} - {self.work_date} - {self.start_time} for {self.hours} hours"



class TestModel(models.Model):
    test_date = models.DateField()
