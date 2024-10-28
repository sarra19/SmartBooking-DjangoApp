from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import PasswordChangeForm


class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        
        fields= ['cin','first_name','last_name','username','email','password1','password2']
        

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        # Ajouter la classe Bootstrap 'form-control' à chaque champ
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

    
    def save(self , commit=True):
        user = super(UserRegisterForm,self).save(commit=False)
        
        if commit:
            user.save()
            
        return user


class PersonForm(UserCreationForm):
    is_superuser = forms.BooleanField(required=False, label="Superuser status")
    class Meta:
        model = get_user_model()
        
        fields= ['cin','first_name','last_name','username','is_superuser', 'email','password1','password2']
        

    def __init__(self, *args, **kwargs):
        super(PersonForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['is_superuser'].widget.attrs['class'] = 'form-check-input'

    
    def save(self , commit=True):
        user = super(PersonForm,self).save(commit=False)
        
        if commit:
            user.save()
            
        return user

class UpdatePersonForm(forms.ModelForm):
    is_superuser = forms.BooleanField(required=False, label="Superuser status")
    class Meta:
        model = get_user_model()
        
        fields= ['cin','first_name','last_name','username','is_superuser']
        

    def __init__(self, *args, **kwargs):
        super(UpdatePersonForm, self).__init__(*args, **kwargs)
        
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        self.fields['is_superuser'].widget.attrs['class'] = 'form-check-input'

    
    def save(self , commit=True):
        user = super(UpdatePersonForm,self).save(commit=False)
        
        if commit:
            user.save()
            
        return user



class PersonUpdateProfileForm(forms.ModelForm):
    image = forms.ImageField(required=False, label="image")
    class Meta:
        model = get_user_model()
        fields = ['username', 'location', 'image']

    def __init__(self, *args, **kwargs):
        super(PersonUpdateProfileForm, self).__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'

        # Personnalisation du champ d'upload d'image
        self.fields['image'].widget.attrs.update({
            'class': 'form-control-file',  # Classe Bootstrap pour le champ de fichier
            'id': 'image'  # Ajout d'un ID pour le JavaScript de prévisualisation si besoin
        })
        
        # Optionnel : Vous pouvez ajouter un placeholder pour donner des instructions
        self.fields['image'].widget.attrs['placeholder'] = 'Téléchargez votre image ici'

    def save(self, commit=True):
        user = super(PersonUpdateProfileForm, self).save(commit=False)
        if commit:
            user.save()
        return user

class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        self.fields['old_password'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter Current password',
            'id': 'id_old_password'  # Assurez-vous d'ajouter un ID
        })
        self.fields['new_password1'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Enter New password',
            'id': 'id_new_password1'  # Assurez-vous d'ajouter un ID
        })
        self.fields['new_password2'].widget.attrs.update({
            'class': 'form-control',
            'placeholder': 'Confirm New password',
            'id': 'id_new_password2'  # Assurez-vous d'ajouter un ID
        })
