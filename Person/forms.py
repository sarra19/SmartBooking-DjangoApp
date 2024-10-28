from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Person
from django.contrib.auth import get_user_model
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
