from django.core.management.base import BaseCommand
from myapp.models import Etudiant, Enseignant, Filiere, Module, Note, Sport, Nationalite
from datetime import date
import random


class Command(BaseCommand):
    help = 'Populate the database with sample data'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS('Starting database population...'))

        # Create Nationalities
        nationalities_data = [
            {'code': 'DZ', 'nationalite': 'Algérienne'},
            {'code': 'FR', 'nationalite': 'Française'},
            {'code': 'MA', 'nationalite': 'Marocaine'},
            {'code': 'TN', 'nationalite': 'Tunisienne'},
            {'code': 'EG', 'nationalite': 'Égyptienne'},
        ]
        
        for nat_data in nationalities_data:
            nationality, created = Nationalite.objects.get_or_create(**nat_data)
            if created:
                self.stdout.write(f'Created nationality: {nationality.nationalite}')

        # Create Sports
        sports_data = ['Football', 'Basketball', 'Tennis', 'Swimming', 'Running', 'Volleyball']
        
        for sport_name in sports_data:
            sport, created = Sport.objects.get_or_create(sport=sport_name)
            if created:
                self.stdout.write(f'Created sport: {sport.sport}')

        # Create Filieres (Academic Programs)
        filieres_data = [
            {'filiere_inscription': 'Informatique', 'description': 'Computer Science and Software Engineering'},
            {'filiere_inscription': 'Mathématiques', 'description': 'Mathematics and Applied Mathematics'},
            {'filiere_inscription': 'Physique', 'description': 'Physics and Applied Physics'},
            {'filiere_inscription': 'Chimie', 'description': 'Chemistry and Chemical Engineering'},
        ]
        
        for filiere_data in filieres_data:
            filiere, created = Filiere.objects.get_or_create(**filiere_data)
            if created:
                self.stdout.write(f'Created filiere: {filiere.filiere_inscription}')

        # Create Teachers
        teachers_data = [
            {
                'email': 'ahmed.benali@university.dz',
                'numero': 1001,
                'civilite': 'Mr',
                'nom': 'Benali',
                'prenom': 'Ahmed',
                'adresse': '123 Rue de l\'Université, Alger',
                'date_naissance': date(1975, 3, 15),
                'lieu_naissance': 'Alger',
                'pays': 'Algérie',
                'grade': 'Professeur',
                'specialite': 'Informatique',
            },
            {
                'email': 'fatima.khadra@university.dz',
                'numero': 1002,
                'civilite': 'Mrs',
                'nom': 'Khadra',
                'prenom': 'Fatima',
                'adresse': '456 Avenue des Sciences, Oran',
                'date_naissance': date(1980, 7, 22),
                'lieu_naissance': 'Oran',
                'pays': 'Algérie',
                'grade': 'MCA',
                'specialite': 'Mathématiques',
            },
            {
                'email': 'mohammed.salem@university.dz',
                'numero': 1003,
                'civilite': 'Mr',
                'nom': 'Salem',
                'prenom': 'Mohammed',
                'adresse': '789 Boulevard de la Paix, Constantine',
                'date_naissance': date(1978, 11, 8),
                'lieu_naissance': 'Constantine',
                'pays': 'Algérie',
                'grade': 'MCB',
                'specialite': 'Physique',
            }
        ]
        
        for teacher_data in teachers_data:
            teacher, created = Enseignant.objects.get_or_create(**teacher_data)
            if created:
                self.stdout.write(f'Created teacher: {teacher.full_name}')

        # Create Modules
        modules_data = [
            {
                'name': 'Programmation Python',
                'coefficient': 3,
                'horaire': 4,
                'filiere': Filiere.objects.get(filiere_inscription='Informatique'),
                'enseignant': Enseignant.objects.get(email='ahmed.benali@university.dz'),
            },
            {
                'name': 'Algorithmes et Structures de Données',
                'coefficient': 4,
                'horaire': 6,
                'filiere': Filiere.objects.get(filiere_inscription='Informatique'),
                'enseignant': Enseignant.objects.get(email='ahmed.benali@university.dz'),
            },
            {
                'name': 'Analyse Mathématique',
                'coefficient': 5,
                'horaire': 5,
                'filiere': Filiere.objects.get(filiere_inscription='Mathématiques'),
                'enseignant': Enseignant.objects.get(email='fatima.khadra@university.dz'),
            },
            {
                'name': 'Algèbre Linéaire',
                'coefficient': 4,
                'horaire': 4,
                'filiere': Filiere.objects.get(filiere_inscription='Mathématiques'),
                'enseignant': Enseignant.objects.get(email='fatima.khadra@university.dz'),
            }
        ]
        
        for module_data in modules_data:
            module, created = Module.objects.get_or_create(**module_data)
            if created:
                self.stdout.write(f'Created module: {module.name}')

        # Create Students
        students_data = [
            {
                'civilite': 'Mr',
                'nom_pre': 'Youssef Boudiaf',
                'date_naissance': date(2000, 5, 12),
                'adresse': '321 Rue des Étudiants, Alger',
                'cod_post': '16000',
                'localite': 'Alger',
                'pays': 'Algérie',
                'plat_form': 'Windows,Linux',
                'applications': 'SGBD,Bureautique',
                'nationalite': Nationalite.objects.get(code='DZ'),
                'filiere': Filiere.objects.get(filiere_inscription='Informatique'),
            },
            {
                'civilite': 'Ms',
                'nom_pre': 'Amina Cherif',
                'date_naissance': date(2001, 2, 18),
                'adresse': '654 Avenue de la République, Oran',
                'cod_post': '31000',
                'localite': 'Oran',
                'pays': 'Algérie',
                'plat_form': 'Mac,Linux',
                'applications': 'DAO,Statistique',
                'nationalite': Nationalite.objects.get(code='DZ'),
                'filiere': Filiere.objects.get(filiere_inscription='Informatique'),
            },
            {
                'civilite': 'Mr',
                'nom_pre': 'Karim Mansouri',
                'date_naissance': date(1999, 9, 30),
                'adresse': '987 Rue de la Science, Constantine',
                'cod_post': '25000',
                'localite': 'Constantine',
                'pays': 'Algérie',
                'plat_form': 'Windows',
                'applications': 'Internet,Bureautique',
                'nationalite': Nationalite.objects.get(code='DZ'),
                'filiere': Filiere.objects.get(filiere_inscription='Mathématiques'),
            },
            {
                'civilite': 'Ms',
                'nom_pre': 'Leila Hamdi',
                'date_naissance': date(2000, 12, 5),
                'adresse': '147 Boulevard des Martyrs, Annaba',
                'cod_post': '23000',
                'localite': 'Annaba',
                'pays': 'Algérie',
                'plat_form': 'Windows,Mac',
                'applications': 'SGBD,DAO',
                'nationalite': Nationalite.objects.get(code='DZ'),
                'filiere': Filiere.objects.get(filiere_inscription='Mathématiques'),
            }
        ]
        
        for student_data in students_data:
            student, created = Etudiant.objects.get_or_create(**student_data)
            if created:
                self.stdout.write(f'Created student: {student.nom_pre}')
                # Add some sports to students
                sports = Sport.objects.all()[:2]
                student.sports.set(sports)

        # Create Notes (Grades)
        students = Etudiant.objects.all()
        modules = Module.objects.all()
        
        for student in students:
            student_modules = modules.filter(filiere=student.filiere)
            for module in student_modules:
                grade = round(random.uniform(8.0, 18.0), 2)
                note, created = Note.objects.get_or_create(
                    etudiant=student,
                    module=module,
                    defaults={'note': grade}
                )
                if created:
                    self.stdout.write(f'Created grade: {student.nom_pre} - {module.name}: {grade}/20')

        self.stdout.write(self.style.SUCCESS('Database population completed successfully!'))
