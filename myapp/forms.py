# myapp/forms.py
from django import forms

from .models import Etudiant, Sport,User

class loginform(forms.ModelForm):
    class Meta:
        model=User
        fields = ('email','password')



class EtudiantForm(forms.ModelForm):
    class Meta:
        model = Etudiant
        fields = '__all__'
        widgets = {
            'plat_form': forms.CheckboxSelectMultiple(choices=[
                ("Windows", "Windows"),
                ("Linux", "Linux"),
                ("Mac", "Mac"),
            ]),
            'date_naissance': forms.SelectDateWidget(years=range(1924,2024)),
            'applications': forms.SelectMultiple(choices=[
                ("SGBD", "SGBD"),
                ("Bureautique", "Bureautique"),
                ("DAO", "DAO"),
                ("Statistique", "Statistique"),
                ("Internet", "Internet"),
            ]),
        }
    sports = forms.ModelMultipleChoiceField(
        queryset=Sport.objects.all(),
        widget=forms.CheckboxSelectMultiple)

class RechercheEtudiantForm(forms.Form):
    numero = forms.IntegerField(label="Numero")