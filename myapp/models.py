from contextlib import nullcontext
from django.db import models
from django.core.exceptions import ValidationError
class Enseignant(models.Model):
    Email = models.EmailField(null=True)
    Numero = models.IntegerField()
    Civilite = models.CharField(max_length=20)
    Nom = models.CharField(max_length=255)
    Prenom = models.CharField(max_length=255)
    Adresse = models.TextField()
    Date_naissance = models.DateField()
    Lieu_naissance = models.CharField(max_length=255)
    Pays = models.CharField(max_length=255)
    Grade = models.CharField(max_length=255)
    Specialite = models.CharField(max_length=255)

    def __str__(self):
        return f"{self.Civilite} {self.Nom} {self.Prenom}, ID: {self.id}"

class Etudiant(models.Model):
    CIVILITY_CHOICES = (
        ('Monsieur', 'Monsieur'),
        ('Madame', 'Madame'),
        ('Mademoiselle', 'Mademoiselle'),
    )

    civilite = models.CharField(max_length=20, choices=CIVILITY_CHOICES)
    nom_pre = models.CharField(max_length=255)
    date_naissance = models.DateField(blank=True, null=True)
    adresse = models.TextField()
    cod_post = models.CharField(max_length=5)
    localite = models.CharField(max_length=255)
    pays = models.CharField(max_length=255)
    plat_form = models.CharField(max_length=255)
    applications = models.CharField(max_length=255)
    nationalite = models.ForeignKey('Nationalite', on_delete=models.SET_NULL, null=True)
    sports = models.ManyToManyField('Sport', blank=True)
    filiere = models.ForeignKey('Filiere', on_delete=models.SET_NULL, null=True)
    image=models.ImageField(upload_to='images/', blank=True, null=True)

    def __str__(self):
        return f"{self.civilite} {self.nom_pre}, ID: {self.id}"

class Nationalite(models.Model):
    code = models.CharField(max_length=10)
    nationalite = models.CharField(max_length=255)
    def __str__(self):
        return f"{self.code} - {self.nationalite}"
    
class Sport(models.Model):
    sport = models.CharField(max_length=255)

    def __str__(self):
        return self.sport

class Filiere(models.Model):
    filiere_inscription = models.CharField(max_length=255)

    def __str__(self):
        return self.filiere_inscription

class Module(models.Model):
    name = models.CharField(max_length=255)
    coefficient = models.IntegerField()
    horaire = models.IntegerField()
    Filiere = models.ForeignKey('Filiere', on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return self.name

class Note(models.Model):
    Etudiant = models.ForeignKey('Etudiant', on_delete=models.SET_NULL, null=True)
    Module = models.ForeignKey('Module', on_delete=models.SET_NULL, null=True)
    Filiere = models.ForeignKey('Filiere', on_delete=models.SET_NULL, null=True, editable=False)
    note = models.FloatField()

    class Meta:
        unique_together = (('Etudiant', 'Module'),)

    def clean(self):
        if self.Etudiant and self.Module and self.Etudiant.filiere != self.Module.Filiere:
            raise ValidationError("The module does not belong to the student's field of study.")

    def save(self, *args, **kwargs):
        if self.Module:
            self.Filiere = self.Module.Filiere
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Name: {self.Etudiant.nom_pre}, branch: {self.Filiere}, module: {self.Module}, grade: {self.note}"
