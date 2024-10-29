from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person
from django.contrib.auth import get_user_model
from django.forms.widgets import ClearableFileInput
from django.contrib.auth.forms import PasswordChangeForm
from django.utils.translation import gettext_lazy as _ 

class UserRegisterForm(UserCreationForm):
    
    class Meta:
        model = get_user_model()
        
        fields= ['cin','first_name','last_name','username','email','keyword', 'password1','password2']
        

    def __init__(self, *args, **kwargs):
        super(UserRegisterForm, self).__init__(*args, **kwargs)
        
        # Ajouter la classe Bootstrap 'form-control' à chaque champ
        for field_name, field in self.fields.items():
            field.widget.attrs['class'] = 'form-control'
        
        self.fields['keyword'].widget.attrs['placeholder'] = 'You can enter a keyword for your password'

    
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
    old_password = forms.CharField(
        label=_("Current password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'current-password'}),
    )
    new_password1 = forms.CharField(
        label=_("New password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'new-password'}),
        help_text=_("Minimum 8 characters long the more, the better, "
                    "At least one lowercase character, "
                    "At least one uppercase character,"
                    "At least one number, symbol, or whitespace character"),
    )
    new_password2 = forms.CharField(
        label=_("Confirm new password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control','autocomplete': 'new-password'}),
    )

    class Meta:
        model = None  # Pas besoin de définir un modèle ici
        fields = ['old_password', 'new_password1', 'new_password2']



class PasswordResetRequestForm(forms.Form):
    email = forms.EmailField(label="Email", max_length=254)



class CustomUserCreationForm(UserCreationForm):
    face_image = forms.ImageField(required=True, label="Image faciale")

    class Meta:
        model = Person
        fields = ['username', 'password1', 'password2', 'face_image']

class FaceLoginForm(forms.Form):
    face_image = forms.ImageField(label='Téléchargez votre image')