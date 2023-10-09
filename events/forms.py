from django import forms
from django.forms.widgets import NumberInput
from .models import WorkShift, Event, Employee
from datetime import time

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        formatted_start_time = obj.start_time.strftime('%d.%m.%Y')
        return f"{formatted_start_time} {obj.name} ({obj.protocol_number})"

class WorkShiftForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        event_id = kwargs.pop('event_id', None)
        super(WorkShiftForm, self).__init__(*args, **kwargs)
        if event_id:
            event = Event.objects.get(id=event_id)
            self.fields['employee'].queryset = Employee.objects.filter(assignment__event_id=event_id)
            self.fields['work_date'].initial = event.start_time.strftime('%Y-%m-%d')
            self.fields['start_time'].initial = time(hour=7, minute=0)

        if 'initial' in kwargs:
            self.fields['event'].initial = kwargs['initial'].get('event')
            self.fields['employee'].initial = kwargs['initial'].get('employee')

    event = CustomModelChoiceField(
        queryset=Event.objects.all().order_by('-start_time'),
        widget=forms.Select(attrs={'class': 'form-select'}),
        label='Wydarzenie'
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_employee'}),
        label='Pracownik'
    )
    work_date = forms.DateField(
        widget=forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date', 'class': 'form-control'}),
        input_formats=('%Y-%m-%d',),
        label='Data'
    )
    start_time = forms.TimeField(
        widget=forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
        label='Start'
    )
    hours = forms.IntegerField(
        widget=NumberInput(attrs={'class': 'form-control', 'min': 1, 'max': 12, 'value': 10}),
        label='L. godzin'
    )

    class Meta:
        model = WorkShift
        fields = ['event', 'employee', 'work_date', 'start_time', 'hours']
