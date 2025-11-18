from django import forms
from .models import Ride, Booking
from datetime import date

class PostRideForm(forms.ModelForm):
    class Meta:
        model = Ride
        fields = ['origin', 'destination', 'seats_available', 'start_date', 'start_time', 'price', 'remarks']
        widgets = {
            'seats_available': forms.NumberInput(attrs={'type': 'number','min': '1','step': '1'}),
            'start_date': forms.DateInput(attrs={'type': 'date',  'min': date.today().strftime('%Y-%m-%d'),}),
            'start_time': forms.TimeInput(attrs={'type': 'time'}),
            'price': forms.NumberInput(attrs={'type': 'number','min': '0.00','step': '0.01'}), # allow decimals
            'remarks': forms.Textarea( attrs={'rows': 3,'placeholder': 'Optional remarks about your ride...'}),
        }



class BookRideForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['num_seats']
        widgets = {
            'num_seats': forms.NumberInput(attrs={'type': 'number', 'min': 1, 'max': 6})
        }