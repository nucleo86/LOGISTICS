import random
import os
import django
from faker import Faker
import sys
from datetime import timedelta


sys.path.append('')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'logistics.settings')
django.setup()

from events.models import Employee, Client, Event, Assignment, Place

fake = Faker("pl_PL")  # Ustawienie języka na polski

# Tworzenie 100 pracowników
for _ in range(100):
    employee = Employee(
        first_name=fake.first_name(),
        last_name=fake.last_name(),
        specialization=fake.job(),
        e_mail=fake.email(),
        phone_number=fake.phone_number()[:15]
    )
    employee.save()

# Wybieranie 5 sprzedawców
sellers = random.sample(list(Employee.objects.all()), 5)

# Wybieranie 5 project managerów
project_managers = random.sample(list(Employee.objects.all()), 5)

# Tworzenie 100 klientów
for _ in range(100):
    client = Client(
        name=fake.company(),
        e_mail=fake.email(),
        phone_number=fake.phone_number()[:15]
    )
    client.save()

# Tworzenie 50 miejsc
for _ in range(50):
    place = Place(
        name=fake.street_name(),
        address=fake.address(),
        e_mail=fake.email()
    )
    place.save()

# Tworzenie 1000 eventów i przypisanie do nich pracowników i klienta
for _ in range(1000):
    start_time = fake.date_this_decade()
    end_time = start_time + timedelta(days=random.randint(1, 21))

    event = Event(
        start_time=start_time,
        end_time=end_time,
        name=fake.bs(),
        protocol_number=fake.bothify(text='???-###', letters='ABCDEFGHIJKLMNOPQRSTUVWXYZ'),
        seller=random.choice(sellers),
        place=random.choice(Place.objects.all())
    )
    event.save()

    # Przypisanie project managera do eventu
    event.project_managers.add(random.choice(project_managers))

    # Przypisanie od 1 do 3 klientów do każdego eventu
    for _ in range(random.randint(1, 3)):
        event.clients.add(random.choice(Client.objects.all()))

    # Przypisanie od 1 do 5 pracowników do każdego eventu
    for _ in range(random.randint(1, 5)):
        assignment = Assignment(
            employee=random.choice(Employee.objects.all()),
            event=event,
            client=random.choice(Client.objects.all())
        )
        assignment.save()

print("Dane zostały wygenerowane!")
