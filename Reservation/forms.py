from django import forms
from django.core.exceptions import ValidationError
from Reservation.models import Reservation
from Flight.models import Flight
from Accommodation.models import Accommodation
from Event.models import Event

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = ['id_flight', 'id_accommodation', 'id_event', 'name_reservation', 'cin', 'phone_number', 'special_requests', 'number_of_travelers', 'passport_numbers']

        widgets = {
            'id_flight': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose a flight...'}),
            'id_accommodation': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose accommodation...'}),
            'id_event': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose event...'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your CIN', 'required': True, 'maxlength': 8, 'minlength': 8, 'pattern': r'^\d{8}$'}),
            'name_reservation': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Reservation Name', 'required': True}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter your phone number', 'required': True, 'maxlength': 8, 'minlength': 8, 'pattern': r'^\d{8}$'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Any special requests...', 'required': False}),
            'passport_numbers': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 8, 'minlength': 8, 'placeholder': 'Enter your passport number (8 characters only)', 'required': True}),
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
        phone_number = cleaned_data.get('phone_number')
        cin = cleaned_data.get('cin')
        passport_numbers = self.data.getlist('passport_numbers[]')
        name_reservation = cleaned_data.get('name_reservation')

        # Validation rules
        if id_event and (id_flight and id_accommodation):
            raise ValidationError("If you choose both a flight and accommodation, you cannot choose an event.")

        if id_event:
            # If an event is selected, do not require number_of_travelers or passport_numbers
            if cleaned_data.get('number_of_travelers'):
                cleaned_data.pop('number_of_travelers')  # Make it optional

            # Clear passport numbers validation
            if passport_numbers:
                for number in passport_numbers:
                    if number.strip() and len(number.strip()) != 8:
                        raise ValidationError("Each passport number must be exactly 8 characters long.")
        
        else:
            # Validation for number_of_travelers and passport_numbers if no event is selected
            number_of_travelers = cleaned_data.get('number_of_travelers')

            if id_flight or id_accommodation:
                # If either flight or accommodation is selected, number_of_travelers must be provided
                if not number_of_travelers:
                    raise ValidationError("Number of travelers is required when selecting a flight or accommodation.")

                # Ensure passport numbers are valid if travelers are specified
                if number_of_travelers and len(passport_numbers) != number_of_travelers:
                    raise ValidationError("You must provide passport numbers for each traveler.")

                for number in passport_numbers:
                    if len(number.strip()) != 8:
                        raise ValidationError("Each passport number must be exactly 8 characters long.")

        # Validate phone number
        if phone_number is None or not str(phone_number).isdigit() or len(str(phone_number).strip()) != 8:
            raise ValidationError("Phone number is required and must be exactly 8 digits long.")

        # Validate CIN number
        if cin is None or not str(cin).isdigit() or len(str(cin).strip()) != 8:
            raise ValidationError("CIN number is required and must be exactly 8 digits long.")

        # Ensure reservation name is provided
        if not name_reservation:
            raise ValidationError("Reservation name is required.")
