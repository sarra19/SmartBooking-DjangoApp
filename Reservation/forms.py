from django import forms
from django.core.exceptions import ValidationError
from Reservation.models import Reservation
from Flight.models import Flight
from Accommodation.models import Accommodation
from Event.models import Event

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id_flight', 'id_accommodation', 'id_event', 'name_reservation', 'cin', 'phone_number', 'special_requests', 'number_of_travelers','passport_numbers']

        widgets = {
            'id_flight': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose a flight...'}),
            'id_accommodation': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose accommodation...'}),
            'id_event': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose event...'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your CIN', 'required': True}),
            'name_reservation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reservation Name', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'required': True, 'maxlength': 8}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests...', 'required': False}),
            'passport_numbers': forms.Textarea(attrs={'rows': 3}),

        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['id_flight'].queryset = Flight.objects.all()
        self.fields['id_accommodation'].queryset = Accommodation.objects.all()
        self.fields['id_event'].queryset = Event.objects.all()

    def clean(self):
        cleaned_data = super().clean()
        id_flight = cleaned_data.get('id_flight')
        id_accommodation = cleaned_data.get('id_accommodation')
        id_event = cleaned_data.get('id_event')

        # Validation logic
        if id_event and (id_flight or id_accommodation):
            raise ValidationError("You cannot choose both an event and a flight/accommodation. Please select only one option.")

        if not id_event and (not id_flight or not id_accommodation):
            raise ValidationError("You must choose either an event or both a flight and accommodation.")

        return cleaned_data
