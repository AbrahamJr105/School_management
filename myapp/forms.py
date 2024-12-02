# myapp/forms.py
from django import forms
from django.contrib.auth.models import User
from .models import Etudiant, Sport, Enseignant,Filiere

class filierepv(forms.Form):
    filiere = forms.ModelChoiceField(queryset=Filiere.objects.all(), empty_label="Select Filiere")

class loginform(forms.ModelForm):
    class Meta:
        model=User
        fields = ('email','password')

class EnseignantForm(forms.ModelForm):
    class Meta:
        model=Enseignant
        fields='__all__'
        widgets = {
            'Civilite': forms.Select(choices=[
                ('Monsieur','Monsieur'),
                ('Madame','Madame'),
                ('Mademoiselle','Mademoiselle'),
            ]),
            'Date_naissance': forms.SelectDateWidget(years=range(1924,2024)),
            'Grade': forms.Select(choices=[
                ('Assistant','Assistant'),
                ('MAB','MAB'),
                ('MAA','MAA'),
                ('MCB','MCB') ,
                ('MCA','MCA'),
                ('Professeur','Professeur')
            ,]),
            'Specialite': forms.Select(choices=[
                ('Informatique','Informatique'),
                ('Mathématiques','Mathématiques'),
                ('Anglais','Anglais'),
                ('autres','autres'),
            ]),
        }

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

class RechercheForm(forms.Form):
    numero = forms.IntegerField(label="Numero")
