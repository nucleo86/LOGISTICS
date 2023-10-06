from django.shortcuts import render, redirect, get_object_or_404
from .models import Event, Employee, Assignment, WorkShift
from django.utils import timezone
from django.core.paginator import Paginator
from django import template
from .forms import WorkShiftForm
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from .forms import TestForm
from collections import defaultdict
from django.db.models import Q

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

def event_list(request):
    event_list = Event.objects.all().order_by('-start_time')

    query = request.GET.get('q')
    if query:
        event_list = event_list.filter(
            Q(name__icontains=query) |
            Q(place__name__icontains=query) |
            Q(place__city__icontains=query) |
            Q(seller__first_name__icontains=query) |
            Q(seller__last_name__icontains=query)
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

    return render(request, 'events/work_shift.html', {'form': form, 'no_employee': no_employee, 'work_shifts': work_shifts})




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

    work_shifts = WorkShift.objects.filter(event_id=event_id, employee_id=employee_id).order_by('work_date', 'start_time').values('work_date', 'start_time', 'hours')
    return JsonResponse(list(work_shifts), safe=False)



def test_view(request):
    if request.method == 'POST':
        form = TestForm(request.POST)
        if form.is_valid():
            form.save()
    else:
        form = TestForm(initial={'test_date': '2023-09-28'})  # Ustawiamy wartość początkową

    return render(request, 'test_template.html', {'form': form})


def get_event_date_range(request, event_id):
    try:
        event = Event.objects.get(id=event_id)
        start_date = event.start_time  # Usunięto .date()
        end_date = event.end_time if event.end_time else None  # Usunięto .date()
        return JsonResponse({'start_date': str(start_date), 'end_date': str(end_date)})
    except Event.DoesNotExist:
        return JsonResponse({'error': 'Event not found'}, status=404)





