from django import forms
from .models import Ride
from datetime import date

class PostRideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin', 'destination', 'seats_available', 'start_date', 'start_time']
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date',  'min': date.today().strftime('%Y-%m-%d'),}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
         }