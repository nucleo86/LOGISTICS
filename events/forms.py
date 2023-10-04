from django import forms
from .models import WorkShift, Event, Employee

class CustomModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        formatted_start_time = obj.start_time.strftime('%d.%m.%Y')
        return f"{formatted_start_time} {obj.name} ({obj.protocol_number})"

class WorkShiftForm(forms.ModelForm):
    event = CustomModelChoiceField(
        queryset=Event.objects.all().order_by('-start_time'),
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    employee = forms.ModelChoiceField(
        queryset=Employee.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_employee'})
    )
    start_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )
    end_time = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={'class': 'form-control', 'type': 'datetime-local'})
    )

    class Meta:
        model = WorkShift
        fields = ['event', 'employee', 'start_time', 'end_time']
