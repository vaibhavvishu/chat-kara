from django import forms
from .models import Booking
from django.utils import timezone

class BookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['event_type', 'event_date', 'event_time', 'number_of_guests', 'event_location', 'special_requirements']
        widgets = {
            'event_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'event_time': forms.TimeInput(attrs={'type': 'time', 'class': 'form-control'}),
            'event_type': forms.Select(attrs={'class': 'form-select'}),
            'number_of_guests': forms.NumberInput(attrs={'class': 'form-control', 'min': '1'}),
            'event_location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Grand Palace Hotel, Mumbai'}),
            'special_requirements': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any dietary preferences or special requests...'}),
        }

    def clean_event_date(self):
        event_date = self.cleaned_data.get('event_date')
        if event_date and event_date < timezone.now().date():
            raise forms.ValidationError("Event date cannot be in the past.")
        return event_date

    def clean_number_of_guests(self):
        guests = self.cleaned_data.get('number_of_guests')
        if guests and guests <= 0:
            raise forms.ValidationError("Number of guests must be a positive number.")
        return guests
