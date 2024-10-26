from django import forms
from .models import Event

class EventForm(forms.ModelForm):
    class Meta:
        model = Event  # Spécifie le modèle à utiliser
        fields = [
            'title',
            'image',
            'location',
            'city',
            'start_date',
            'end_date',
            'description',
            'price_per_place',
            'number_places',
        ]  # Liste des champs à inclure dans le formulaire

        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Champ pour la date et l'heure de début
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),  # Champ pour la date et l'heure de fin
            'description': forms.Textarea(attrs={'rows': 4, 'cols': 40}),  # Champ de description
        }

    def clean(self):
        cleaned_data = super().clean()
        start_date = cleaned_data.get("start_date")
        end_date = cleaned_data.get("end_date")

        # Validation que la date de fin est après la date de début
        if start_date and end_date and start_date >= end_date:
            raise forms.ValidationError("La date de fin doit être postérieure à la date de début.")

        return cleaned_data
