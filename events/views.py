from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Employee, Assignment, WorkShift
from django.utils import timezone
from django.core.paginator import Paginator
from django import template
from .forms import WorkShiftForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from collections import defaultdict
from django.db.models import Q
from datetime import timedelta
import logging

register = template.Library()
logger = logging.getLogger(__name__)

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


def event_list(request):
    event_list = Event.objects.all().order_by('-start_time').select_related("place", "seller")

    user_input = request.GET.get('q')
    if user_input:
        event_list = event_list.filter(
            Q(name__icontains=user_input) |
            Q(place__name__icontains=user_input) |
            Q(place__city__icontains=user_input) |
            Q(seller__first_name__icontains=user_input) |
            Q(seller__last_name__icontains=user_input)
        )

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date:
        start_datetime = timezone.datetime.strptime(from_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        event_list = event_list.filter(start_time__gte=start_datetime)

    if to_date:
        end_datetime = timezone.datetime.strptime(to_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        event_list = event_list.filter(end_time__lte=end_datetime)

    paginator = Paginator(event_list, 20)
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'events': events
    }

    return render(request, 'events/event_list.html', context)


def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    assignments = Assignment.objects.filter(event=event).select_related('role')

    # Znajdź następny i poprzedni event
    next_event = Event.objects.filter(start_time__gt=event.start_time).order_by('start_time').first()
    prev_event = Event.objects.filter(start_time__lt=event.start_time).order_by('-start_time').first()

    # Grupowanie przyporządkowań według roli
    assignments_by_role = defaultdict(list)
    for assignment in assignments:
        role_name = assignment.role.name if assignment.role else 'Brak'
        assignments_by_role[role_name].append(assignment)

    context = {
        'event': event,
        'next_event': prev_event,
        'prev_event': next_event,
        'assignments': assignments,
        'assignments_by_role': dict(assignments_by_role)  # Konwersja na zwykły słownik
    }

    return render(request, 'events/event_detail.html', context)


def employee_detail(request, pk):
    employee = get_object_or_404(Employee, id=pk)
    assignments = Assignment.objects.filter(employee=employee)
    events = [assignment.event for assignment in assignments]

    # Sortowanie wydarzeń od najnowszego do najstarszego, zakładając, że pole `start_time` istnieje w modelu Event
    events = sorted(events, key=lambda x: x.start_time, reverse=True)

    context = {
        'employee': employee,
        'assignments': assignments,
        'events': events
    }

    return render(request, 'events/employee_detail.html', context)


def work_shift(request, event_id, employee_id):
    try:
        event = Event.objects.get(id=event_id)
        employee = Employee.objects.get(id=employee_id)
        initial_data = {
            'event': event,
            'employee': employee,
            'work_date': event.start_time,
        }
    except ObjectDoesNotExist:
        initial_data = {}

    no_employee = False
    if 'event' in initial_data:
        employees_for_event = Employee.objects.filter(assignment__event_id=event_id)
        if not employees_for_event.exists():
            no_employee = True

    # Pobranie wszystkich zmian pracy dla danego wydarzenia i pracownika
    work_shifts = WorkShift.objects.filter(event_id=event_id, employee_id=employee_id)

    if request.method == 'POST':
        form = WorkShiftForm(request.POST, initial=initial_data, event_id=event_id)
        if form.is_valid():
            form.save()
            initial_data['employee'] = form.cleaned_data['employee']
            form = WorkShiftForm(initial=initial_data, event_id=event_id)

    else:
        form = WorkShiftForm(initial=initial_data, event_id=event_id)

    return render(request, 'events/work_shift.html',
                  {'form': form, 'no_employee': no_employee, 'work_shifts': work_shifts})


def get_first_employee_for_event(request, event_id):
    employees = Employee.objects.filter(assignment__event_id=event_id)
    if employees.exists():
        first_employee = employees.first()
        return JsonResponse({'first_employee_id': first_employee.id})
    else:
        return JsonResponse({'first_employee_id': None})


def get_work_shifts(request):
    event_id = request.GET.get('event_id', None)
    employee_id = request.GET.get('employee_id', None)

    if event_id is None or employee_id is None:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    work_shifts = WorkShift.objects.filter(event_id=event_id, employee_id=employee_id).order_by('work_date',
                                                                                                'start_time').values(
        'work_date', 'start_time', 'hours')
    return JsonResponse(list(work_shifts), safe=False)


def get_event_date_range(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        start_date = event.start_time
        end_date = event.end_time if event.end_time else None
        return JsonResponse({'start_date': str(start_date), 'end_date': str(end_date)})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)



def employee_availability(request):
    # Odczytaj daty z parametrów GET lub użyj domyślnych wartości
    start_date_str = request.GET.get('start_date', None)
    end_date_str = request.GET.get('end_date', None)

    if start_date_str and end_date_str:
        start_date = timezone.datetime.strptime(start_date_str, '%Y-%m-%d').date()
        end_date = timezone.datetime.strptime(end_date_str, '%Y-%m-%d').date()
    else:
        now = timezone.now().date()
        start_date = now - timedelta(days=10)
        end_date = now

    query = request.GET.get('q', None)

    base_employee_query = Employee.objects.select_related('department')
    base_event_query = Event.objects.filter(
        start_time__lte=end_date,
        end_time__gte=start_date
    )

    if query:
        employees = base_employee_query.filter(
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query) |
            Q(department__name__icontains=query) |
            Q(groups__name__icontains=query)
        ).distinct()

        all_events = base_event_query.filter(
            Q(name__icontains=query) |
            Q(protocol_number__icontains=query) |
            Q(seller__first_name__icontains=query) |
            Q(seller__last_name__icontains=query)
        )
    else:
        employees = base_employee_query.all()
        all_events = base_event_query

    data = []

    for employee in employees:
        events = Event.objects.filter(
            assignment__employee=employee,
            start_time__lte=end_date,
            end_time__gte=start_date
        )
        work_shifts = WorkShift.objects.filter(
            employee=employee,
            work_date__range=[start_date, end_date]
        )

        employee_data = {
            "id": employee.id,
            "name": str(employee),
            "department": str(employee.department) if employee.department else None,
            "groups": ", ".join([str(group) for group in employee.groups.all()]) if employee.groups.exists() else None,
            "events": [
                {
                    "id": event.id,
                    "name": event.name,
                    "start_time": event.start_time,
                    "end_time": event.end_time,
                }
                for event in events
            ],
            "work_shifts": [
                {
                    "id": work_shift.id,
                    "event_id": work_shift.event.id,
                    "event": str(work_shift.event.name),
                    "work_date": work_shift.work_date,
                    "start_time": work_shift.start_time,
                    "hours": work_shift.hours,
                }
                for work_shift in work_shifts
            ],
        }
        data.append(employee_data)

    return JsonResponse({
        "employees": data,
        "start_date": start_date,
        "end_date": end_date,
        "all_events": [{"id": event.id, "name": event.name, "start_time": event.start_time, "end_time": event.end_time}
                       for event in all_events],
    })


def employee_availability_table(request):
    return render(request, 'employee_availability.html')

