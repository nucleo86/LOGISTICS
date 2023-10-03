from django.shortcuts import render, get_object_or_404
from .models import Event, Employee, Assignment
from django.utils import timezone
from django.core.paginator import Paginator
from django import template

register = template.Library()

@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)

def event_list(request):
    event_list = Event.objects.all().order_by('-start_time')

    query = request.GET.get('q')
    if query:
        event_list = event_list.filter(name__icontains=query)

    from_date = request.GET.get('from_date')
    to_date = request.GET.get('to_date')

    if from_date:
        start_datetime = timezone.datetime.strptime(from_date + " 00:00:00", "%Y-%m-%d %H:%M:%S")
        event_list = event_list.filter(start_time__gte=start_datetime)

    if to_date:
        end_datetime = timezone.datetime.strptime(to_date + " 23:59:59", "%Y-%m-%d %H:%M:%S")
        event_list = event_list.filter(end_time__lte=end_datetime)

    paginator = Paginator(event_list, 25)  # Pokaż 25 eventów na stronę
    page = request.GET.get('page')
    events = paginator.get_page(page)

    context = {
        'events': events
    }

    return render(request, 'events/event_list.html', context)



def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    assignments = Assignment.objects.filter(event=event)
    return render(request, 'events/event_detail.html', {'event': event, 'assignments': assignments})

