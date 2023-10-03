import os
import openpyxl
import django

# Ustawienie zmiennej środowiskowej DJANGO_SETTINGS_MODULE
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "logistics.settings")

# Inicjowanie Django
django.setup()

from events.models import Event, Client, Employee

# Otwieranie pliku Excela
wb = openpyxl.load_workbook('events.xlsx')
sheet = wb.active

# Przechodzenie przez każdy wiersz w arkuszu (pomijając nagłówek)
for row in sheet.iter_rows(min_row=2, values_only=True):
    date, client_name, protocol_number, project_manager_name, seller_name, name_in_excel = row[:6]  # Uwzględnienie kolumny F

    # Tworzenie lub pobieranie istniejącego klienta
    if client_name:
        client, created = Client.objects.get_or_create(name=client_name)
    else:
        client = None

    # Próbujemy znaleźć Project Managera i Sprzedawcę w modelu Employee
    if project_manager_name:
        names = project_manager_name.split()
        first_name = names[0] if len(names) > 0 else ""
        last_name = names[1] if len(names) > 1 else ""

        try:
            project_manager = Employee.objects.get(first_name=first_name, last_name=last_name)
        except Employee.DoesNotExist:
            project_manager = None
    else:
        project_manager = None

    if seller_name:
        names = seller_name.split()
        first_name = names[0] if len(names) > 0 else ""
        last_name = names[1] if len(names) > 1 else ""

        try:
            seller = Employee.objects.get(first_name=first_name, last_name=last_name)
        except Employee.DoesNotExist:
            seller = None
    else:
        seller = None

    if protocol_number is None:
        protocol_number = ""  # Ustawia domyślną wartość

    # Tworzenie nowego eventu
    event = Event(
        start_time=date,
        name_in_excel=name_in_excel,
        protocol_number=protocol_number,
        client=client,
        project_manager=project_manager,
        seller=seller
    )
    event.save()
