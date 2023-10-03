from django import forms
from .models import WorkShift, Event

class WorkShiftForm(forms.ModelForm):
    event = forms.ModelChoiceField(
        queryset=Event.objects.all(),
        widget=forms.Select(attrs={'class': 'form-select'})
    )

    class Meta:
        model = WorkShift
        fields = ['event', 'start_time', 'end_time']
