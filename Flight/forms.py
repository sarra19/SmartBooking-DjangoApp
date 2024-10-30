from django import forms
from .models import Flight

class FlightForm(forms.ModelForm):
    class Meta:
        model = Flight
        fields = [
            'flight_name', 
            'image', 
            'flight_number', 
            'departure_city', 
            'arrival_city', 
            'departure_date', 
            'arrival_date', 
            'airline', 
            'price_per_place', 
           
        ]
        
        # Optional: You can customize the widgets (HTML input types) for each field if needed
        widgets = {
            'departure_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'arrival_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }