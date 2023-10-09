import random
import os
import django
from faker import Faker
import sys
from datetime import timedelta, datetime

sys.path.append('')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics.settings')
django.setup()

from events.models import Employee, Client, Event, Assignment, Place, Specialization, Group, Department, EmployeeSpecialization, WorkShift

# Usuwanie wszystkich rekordów z modeli
WorkShift.objects.all().delete()
EmployeeSpecialization.objects.all().delete()
Employee.objects.all().delete()
Client.objects.all().delete()
Event.objects.all().delete()
Assignment.objects.all().delete()
Place.objects.all().delete()
Specialization.objects.all().delete()
Group.objects.all().delete()
Department.objects.all().delete()

fake = Faker("pl_PL")  # Ustawienie języka na polski

# Adding fixed values for Department, Group, Specialization
for name in ["Rental", "IT", "Instalacje", "Magazyn"]:
    Department.objects.get_or_create(name=name)
for name in ["Technik", "Realizator", "Informatyk", "Grafik", "Project manager", "Handlowiec"]:
    Group.objects.get_or_create(name=name)
for name in ["Światło", "Dźwięk", "Grafika", "Podnośniki", "Sieci komputerowe"]:
    Specialization.objects.get_or_create(name=name)

# Generate employees and their specializations
for _ in range(100):
    employee = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        e_mail=fake.email(),
        phone_number=fake.phone_number()[:15],
        department=random.choice(list(Department.objects.all()))
    )
    employee.save()
    employee.groups.set(random.sample(list(Group.objects.all()), k=random.randint(1, len(Group.objects.all()))))

    # Assigning 1-5 random specializations to the employee with random skill levels
    specializations = random.sample(list(Specialization.objects.all()), k=random.randint(1, 5))
    for specialization in specializations:
        EmployeeSpecialization.objects.create(
            employee=employee,
            specialization=specialization,
            skill_level=random.randint(1, 3)
        )

# Generate Clients
for _ in range(100):
    client = Client(
        name=" ".join(fake.bs().upper().split()[:2]),
        e_mail=fake.email(),
        phone_number=fake.phone_number()[:15]
    )
    client.save()

# Generate Places
for _ in range(50):
    place = Place(
        name=" ".join(fake.bs().upper().split()[:2]),
        street=fake.street_address(),
        postal_code=fake.postalcode(),
        city=fake.city(),
        e_mail=fake.email()
    )
    place.save()

# Generate Events
for _ in range(500):
    start_time = fake.date_this_decade()
    end_time = start_time + timedelta(days=random.randint(3, 21))
    event = Event(
        start_time=start_time,
        end_time=end_time,
        name=" ".join(fake.bs().upper().split()[:2]),
        protocol_number="REORWAR20" + str(random.randint(1000, 9999)),
        seller=random.choice(list(Employee.objects.filter(groups__name="Handlowiec"))),
        place=random.choice(Place.objects.all())
    )
    event.save()
    event.project_managers.add(random.choice(list(Employee.objects.filter(groups__name="Project manager"))))
    event.clients.add(*random.sample(list(Client.objects.all()), k=random.randint(1, 3)))

    # Generowanie Assignments i WorkShifts
    for _ in range(random.randint(3, 21)):
        assignment_employee = random.choice(Employee.objects.all())
        assignment = Assignment(
            employee=assignment_employee,
            event=event,
            client=random.choice(Client.objects.all())
        )
        # Wybierz jedną z dostępnych specjalizacji dla tego pracownika
        available_specializations = EmployeeSpecialization.objects.filter(employee=assignment_employee)
        if available_specializations.exists():
            chosen_role = random.choice(available_specializations).specialization
            assignment.role = chosen_role
        assignment.save()

        # Generowanie WorkShifts
        work_dates = set()  # Tworzenie zbioru dat
        while len(work_dates) < 3:  # Minimalnie 3 różne daty
            work_date = fake.date_between_dates(date_start=event.start_time, date_end=event.end_time)
            work_dates.add(work_date)

        for work_date in work_dates:
            start_time_str = fake.time()
            start_time = datetime.strptime(start_time_str, '%H:%M:%S').time()
            hours = random.randint(6, 14)  # Losowa liczba godzin, możesz dostosować

            work_shift = WorkShift(
                employee=assignment.employee,
                event=event,
                work_date=work_date,
                start_time=start_time,
                hours=hours
            )
            work_shift.save()


print("Dane zostały wygenerowane!")
