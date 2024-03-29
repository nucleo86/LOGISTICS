from django.db import models

class Department(models.Model):
    """Represents a department in an organization."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Specialization(models.Model):
    """Represents a specialization field."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Group(models.Model):
    """Represents a group within an organization or department."""
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Employee(models.Model):
    """Represents an employee."""
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100, null=True, blank=True)
    e_mail = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, blank=True)
    employment_status = models.BooleanField(default=True)
    groups = models.ManyToManyField(Group, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class EmployeeSpecialization(models.Model):
    """Represents an employee's specialization."""
    LEVELS = [
        (1, 'Beginner'),
        (2, 'Intermediate'),
        (3, 'Advanced'),
    ]

    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    specialization = models.ForeignKey(Specialization, on_delete=models.CASCADE)
    skill_level = models.IntegerField(choices=LEVELS)

    def __str__(self):
        return f"{self.employee} - {self.specialization} - Level {self.skill_level}"



class Client(models.Model):
    name = models.CharField(max_length=255)
    e_mail = models.EmailField(null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)

    def __str__(self):
        return self.name

class Place(models.Model):
    name = models.CharField(max_length=255)
    street = models.CharField(max_length=255,null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    e_mail = models.EmailField(null=True, blank=True)

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
        return f"{self.name or ''}"

class Assignment(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, null=True, blank=True)
    role = models.ForeignKey(Specialization, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.employee} assigned to {self.event} as {self.role}"

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
        return f"{self.event.name}"
