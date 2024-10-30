from django import forms
from .models import Accommodation

class AccommodationForm(forms.ModelForm):
    class Meta:
        model = Accommodation
        fields = '__all__'
        labels = {
            'name': 'Nom de l’hébergement',
            'image': 'Image',
            'location': 'Localisation',
            'description': 'Description',
            'type_of_accommodation': 'Type d’hébergement',
            'price_per_night': 'Prix par nuit',
            'amenities': 'Équipements',
            'rating': 'Évaluation',
        }
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'image': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'type_of_accommodation': forms.Select(attrs={'class': 'form-select'}),
            'price_per_night': forms.NumberInput(attrs={'class': 'form-control'}),
            'amenities': forms.CheckboxSelectMultiple(),  # Pour la sélection multiple
            'rating': forms.RadioSelect(choices=[(i, f"{i} étoiles") for i in range(1, 6)]),  # Options pour l'évaluation
        }

