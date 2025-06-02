# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Filiere


class filierepv(forms.Form):
    """Form for selecting a field of study for PV generation."""
    filiere = forms.ModelChoiceField(
        queryset=Filiere.objects.all(), 
        empty_label="Sélectionner une filière",
        widget=forms.Select(attrs={
            'class': 'form-control',
            'required': True
        })
    )


class loginform(forms.ModelForm):
    """Form for user authentication."""
    
    class Meta:
        model = User
        fields = ('email', 'password')
        widgets = {
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre email',
                'required': True
            }),
            'password': forms.PasswordInput(attrs={
                'class': 'form-control',
                'placeholder': 'Entrez votre mot de passe',
                'required': True
            })
        }



