from django import forms
from django.core.exceptions import ValidationError
from Reservation.models import Reservation
from Flight.models import Flight
from Accommodation.models import Accommodation
from Event.models import Event

class ReservationForm(forms.ModelForm):
    class Meta:
        model = Reservation
        fields = [
            'id_flight', 'id_accommodation', 'id_event', 'name_reservation', 
            'cin', 'phone_number', 'special_requests', 'number_of_travelers', 
            'passport_numbers','status','prompt','reservinfo'
        ]

        widgets = {
            'id_flight': forms.Select(attrs={'class': 'form-select'}),
            'id_accommodation': forms.Select(attrs={'class': 'form-select'}),
            'id_event': forms.Select(attrs={'class': 'form-select'}),
            'cin': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 8}),
            'name_reservation': forms.TextInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'maxlength': 8}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select', 'placeholder': 'Choose status...'}),
            'special_requests': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'passport_numbers': forms.Textarea(attrs={'class': 'form-control', 'rows': 2, 'placeholder': 'Enter passport numbers, one per line'}),  # Added widget
            'reservinfo': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'placeholder': 'Enter additional reservation info as JSON'}),  # New widget for reservinfo
            'prompt': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),

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
        number_of_travelers = cleaned_data.get('number_of_travelers')
       
        

        if id_event and (id_flight or id_accommodation):
            raise ValidationError("Selecting both a flight and accommodation excludes event selection.")

        if id_event:
            if number_of_travelers:
                cleaned_data.pop('number_of_travelers')
            if passport_numbers:
                for number in passport_numbers:
                    if len(number.strip()) != 8:
                        raise ValidationError("Each passport number must be exactly 8 characters.")

        elif (id_flight or id_accommodation):
            if not number_of_travelers:
                raise ValidationError("Specify the number of travelers when choosing a flight or accommodation.")
            if len(passport_numbers) != int(number_of_travelers):
                raise ValidationError("Provide exactly one passport number per traveler.")
            for number in passport_numbers:
                if len(number.strip()) != 8:
                    raise ValidationError("Each passport number must be exactly 8 characters.")

        if phone_number is None or not str(phone_number).isdigit() or len(str(phone_number).strip()) != 8:
            raise ValidationError("Phone number must be exactly 8 digits.")
        if cin is None or not str(cin).isdigit() or len(str(cin).strip()) != 8:
            raise ValidationError("CIN number must be exactly 8 digits.")
        if not name_reservation:
            raise ValidationError("Reservation name is required.")
        # if not id_flight and not id_accommodation and not id_event:
        #     raise ValidationError("Please select at least one option: Flight, Accommodation, or Event.")
     