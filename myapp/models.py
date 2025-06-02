from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator, MaxValueValidator


class Enseignant(models.Model):
    """Model representing a teacher/instructor."""
    
    CIVILITY_CHOICES = [
        ('Mr', 'Monsieur'),
        ('Mrs', 'Madame'),
        ('Ms', 'Mademoiselle'),
    ]
    
    GRADE_CHOICES = [
        ('Assistant', 'Assistant'),
        ('MAB', 'Maître Assistant B'),
        ('MAA', 'Maître Assistant A'),
        ('MCB', 'Maître de Conférences B'),
        ('MCA', 'Maître de Conférences A'),
        ('Professeur', 'Professeur'),
    ]
    
    SPECIALTY_CHOICES = [
        ('Informatique', 'Informatique'),        ('Mathématiques', 'Mathématiques'),
        ('Anglais', 'Anglais'),
        ('Physique', 'Physique'),
        ('Chimie', 'Chimie'),
        ('autres', 'Autres'),
    ]

    email = models.EmailField(unique=True, help_text="Email address of the teacher")
    numero = models.IntegerField(unique=True, help_text="Teacher identification number")
    civilite = models.CharField(max_length=20, choices=CIVILITY_CHOICES, verbose_name="Civility")
    nom = models.CharField(max_length=255, verbose_name="Last Name")
    prenom = models.CharField(max_length=255, verbose_name="First Name")
    adresse = models.TextField(verbose_name="Address", default="Address not provided")
    date_naissance = models.DateField(verbose_name="Date of Birth", null=True, blank=True)
    lieu_naissance = models.CharField(max_length=255, verbose_name="Place of Birth", default="Not specified")
    pays = models.CharField(max_length=255, verbose_name="Country")
    grade = models.CharField(max_length=255, choices=GRADE_CHOICES, verbose_name="Academic Grade")
    specialite = models.CharField(max_length=255, choices=SPECIALTY_CHOICES, verbose_name="Specialty")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Enseignant"
        verbose_name_plural = "Enseignants"
        ordering = ['nom', 'prenom']

    def __str__(self):
        return f"{self.civilite} {self.nom} {self.prenom} - {self.grade}"

    @property
    def full_name(self):
        return f"{self.prenom} {self.nom}"

class Etudiant(models.Model):
    """Model representing a student."""
    
    CIVILITY_CHOICES = [
        ('Mr', 'Monsieur'),
        ('Mrs', 'Madame'),
        ('Ms', 'Mademoiselle'),
    ]

    civilite = models.CharField(max_length=20, choices=CIVILITY_CHOICES, verbose_name="Civility")
    nom_pre = models.CharField(max_length=255, verbose_name="Full Name")
    date_naissance = models.DateField(blank=True, null=True, verbose_name="Date of Birth")
    adresse = models.TextField(verbose_name="Address")
    cod_post = models.CharField(max_length=10, verbose_name="Postal Code")
    localite = models.CharField(max_length=255, verbose_name="City")
    pays = models.CharField(max_length=255, verbose_name="Country")
    plat_form = models.CharField(max_length=255, verbose_name="Platforms", help_text="Comma-separated platforms")
    applications = models.CharField(max_length=255, verbose_name="Applications", help_text="Comma-separated applications")
    nationalite = models.ForeignKey('Nationalite', on_delete=models.SET_NULL, null=True, verbose_name="Nationality")
    sports = models.ManyToManyField('Sport', blank=True, verbose_name="Sports")
    filiere = models.ForeignKey('Filiere', on_delete=models.SET_NULL, null=True, verbose_name="Field of Study")
    image = models.ImageField(upload_to='students/', blank=True, null=True, verbose_name="Photo")
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Étudiant"
        verbose_name_plural = "Étudiants"
        ordering = ['nom_pre']

    def __str__(self):
        return f"{self.civilite} {self.nom_pre} - {self.filiere}"

    def clean(self):
        if self.cod_post and not self.cod_post.isdigit():
            raise ValidationError({'cod_post': 'Postal code must contain only digits.'})

    @property
    def average_grade(self):
        """Calculate the weighted average grade for this student."""
        from django.db.models import Sum, F
        notes = Note.objects.filter(etudiant=self)
        if not notes.exists():
            return 0
        
        weighted_sum = notes.aggregate(
            total=Sum(F('note') * F('module__coefficient'))
        )['total'] or 0
        
        total_coefficient = notes.aggregate(
            total=Sum('module__coefficient')
        )['total'] or 1
        
        return round(weighted_sum / total_coefficient, 2)

class Nationalite(models.Model):
    """Model representing nationality information."""
    
    code = models.CharField(max_length=10, unique=True, verbose_name="Country Code")
    nationalite = models.CharField(max_length=255, unique=True, verbose_name="Nationality")
    
    class Meta:
        verbose_name = "Nationalité"
        verbose_name_plural = "Nationalités"
        ordering = ['nationalite']

    def __str__(self):
        return f"{self.code} - {self.nationalite}"


class Sport(models.Model):
    """Model representing sports activities."""
    
    sport = models.CharField(max_length=255, unique=True, verbose_name="Sport Name")
    
    class Meta:
        verbose_name = "Sport"
        verbose_name_plural = "Sports"
        ordering = ['sport']

    def __str__(self):
        return self.sport


class Filiere(models.Model):
    """Model representing academic fields of study."""
    
    filiere_inscription = models.CharField(max_length=255, unique=True, verbose_name="Field of Study")
    description = models.TextField(blank=True, null=True, verbose_name="Description")
    
    class Meta:
        verbose_name = "Filière"
        verbose_name_plural = "Filières"
        ordering = ['filiere_inscription']

    def __str__(self):
        return self.filiere_inscription


class Module(models.Model):
    """Model representing academic modules/courses."""
    
    name = models.CharField(max_length=255, verbose_name="Module Name")
    coefficient = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name="Coefficient"
    )
    horaire = models.IntegerField(
        validators=[MinValueValidator(1)],
        verbose_name="Hours per Week"
    )
    filiere = models.ForeignKey(
        'Filiere', 
        on_delete=models.CASCADE, 
        verbose_name="Field of Study",
        related_name='modules'
    )
    enseignant = models.ForeignKey(
        'Enseignant',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        verbose_name="Teacher",
        related_name='modules'
    )
    
    class Meta:
        verbose_name = "Module"
        verbose_name_plural = "Modules"
        unique_together = [['name', 'filiere']]
        ordering = ['filiere', 'name']

    def __str__(self):
        return f"{self.name} ({self.filiere})"


class Note(models.Model):
    """Model representing student grades."""
    
    etudiant = models.ForeignKey(
        'Etudiant', 
        on_delete=models.CASCADE, 
        verbose_name="Student",
        related_name='notes'
    )
    module = models.ForeignKey(
        'Module', 
        on_delete=models.CASCADE, 
        verbose_name="Module",
        related_name='notes'
    )
    filiere = models.ForeignKey(
        'Filiere', 
        on_delete=models.CASCADE, 
        editable=False,
        verbose_name="Field of Study"
    )
    note = models.FloatField(
        validators=[MinValueValidator(0), MaxValueValidator(20)],
        verbose_name="Grade"
    )
    date_evaluation = models.DateField(auto_now_add=True, verbose_name="Evaluation Date")

    class Meta:
        verbose_name = "Note"
        verbose_name_plural = "Notes"
        unique_together = [['etudiant', 'module']]
        ordering = ['-date_evaluation']

    def clean(self):
        if self.etudiant and self.module:
            if self.etudiant.filiere != self.module.filiere:
                raise ValidationError(
                    "The module does not belong to the student's field of study."
                )

    def save(self, *args, **kwargs):
        if self.module:
            self.filiere = self.module.filiere
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.etudiant.nom_pre} - {self.module.name}: {self.note}/20"

    @property
    def is_passing(self):
        return self.note >= 10

    @property
    def weighted_grade(self):
        return self.note * self.module.coefficient