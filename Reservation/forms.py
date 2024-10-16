from django import forms
from Reservation.models import Reservation
from Flight.models import Flight
from Accommodation.models import Accommodation
from RentalTransport.models import RentalTransport

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id_flight', 'id_accommodation', 'id_transport', 'name_reservation', 'cin', 'phone_number', 'special_requests']
        
        widgets = {
            'id_flight': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose a flight...'}),
            'id_accommodation': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose accommodation...'}),
            'id_transport': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose transport...'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your CIN', 'required': True}),
            'name_reservation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reservation Name', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'required': True, 'maxlength': 8}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests...', 'required': False}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_flight'].queryset = Flight.objects.all()
        self.fields['id_accommodation'].queryset = Accommodation.objects.all()
        self.fields['id_transport'].queryset = RentalTransport.objects.all()
