import os

from django.core.mail import send_mail
from django.http import HttpResponse
from django.shortcuts import redirect
from dotenv import load_dotenv
from .forms import EtudiantForm, RechercheEtudiantForm, loginform
from .models import User
load_dotenv()

def login(request):
    if request.method == 'POST':
            user = User.objects.get(email=request.POST['email'])
            if request.POST['password']==user.password:
                if user.role == 'admin':
                    return redirect("/")
                else:
                    return redirect("/bulletin")
            else:
                return HttpResponse("Wrong password")
    else:
        form = loginform()
    return render(request, 'login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = request.POST.get('role')
            user.save()
            return redirect('login')
    else:
        form = loginform()
    return render(request, 'register.html', {'form': form})

def menu(request):
    return render(request, 'menu.html')

def etudiant_form(request):
    if request.method == 'POST':
        if 'Enregistrer' in request.POST:
            form = EtudiantForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Saved.')
            else:
                return render(request, 'etudiant_form.html', {'form': form})
        elif 'rechercher' in request.POST:
            search_form = RechercheEtudiantForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['numero']
                try:
                    etudiant = Etudiant.objects.get(pk=search_id)
                    return render(request, 'etudiant_form.html', {'etudiant': etudiant})
                except Etudiant.DoesNotExist:
                    return HttpResponse("mf was not found")
            else:
                print(search_form.errors)
        elif 'supprimer' in request.POST:
            search_form = RechercheEtudiantForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['numero']
                try:
                    etudiant = Etudiant.objects.get(pk=search_id)
                    etudiant.delete()
                    return redirect('etudiant_form')
                except Etudiant.DoesNotExist:
                    error_message = "Etudiant introuvable."
                    return render(request, 'etudiant_form.html', {'error_message': error_message})
        elif 'modifier' in request.POST:
            search_id = request.POST.get('Numero')
            try:
                etudiant = Etudiant.objects.get(pk=search_id)
                if search_id and request.POST:
                    form = EtudiantForm(request.POST, instance=etudiant)
                    if form.is_valid():
                        form.save()
                        return redirect('etudiant_form')
                    else:
                        print(form.errors)
            except Etudiant.DoesNotExist:
                error_message = "Etudiant introuvable."
                return render(request, 'etudiant_form.html', {'error_message': error_message})
    else:
        form=EtudiantForm()
        search_form=RechercheEtudiantForm()
        return render(request, 'etudiant_form.html',{"search_form":search_form,'form': form})

from django.db.models import F


def pv(request):
    etudiants = Etudiant.objects.all()
    student_grades = []
    passinggrades=0
    failinggrades=0
    for etudiant in etudiants:
        weighted_sum_of_notes = Note.objects.filter(Etudiant=etudiant).annotate(
            weighted_note=F('note') * F('Module__coefficient')
        ).aggregate(total_weighted=Sum('weighted_note'))['total_weighted'] or 0

        sum_of_coefficients = Module.objects.filter(Filiere=etudiant.filiere).aggregate(
            total_coefficient=Sum('coefficient')
        )['total_coefficient'] or 1

        average_grade = weighted_sum_of_notes / sum_of_coefficients

        student_grades.append({
            'student': etudiant,
            'average_grade': average_grade
        })
        if average_grade >=10:
            passinggrades+=1
        else:
            failinggrades+=1

    return render(request, 'pv.html', {'student_grades': student_grades, 'passinggrades': passinggrades, 'failinggrades': failinggrades})
def statistique(request):
    all=Etudiant.objects.all().count()
    male = Etudiant.objects.filter(civilite="Monsieur").count()
    female = all-male
    all2 = User.objects.all().count()
    user = User.objects.filter(role="user").count()
    admin = all2 - user
    return render(request, 'statistique.html', {'male': male, 'female': female, 'all': all, 'user': user, 'admin': admin, "all2": all2})





from django.shortcuts import render, get_object_or_404
from .models import Etudiant, Note, Module
from django.db.models import Sum

def bulletin_view(request):
    if request.method == 'POST' :
        if 'bulletin' in request.POST:
            idetu = request.POST.get('num')
            etudiant = get_object_or_404(Etudiant, id=idetu)
            notes = Note.objects.filter(Etudiant_id=idetu)
            statistiques = notes.aggregate(
                SommeCoefficient=Sum(F('Module__coefficient')),
                SommeCoiNotes=Sum(F('Module__coefficient') * F('note')),
                moyenne=Sum(F('Module__coefficient') * F('note')) / Sum('Module__coefficient')
            )
            return render(request, 'bulletin.html', {
                'etudiant': etudiant,
                'notes': notes,
                'statistiques': statistiques,
            })
        else:
            send_mail(
                'Subject: Message from Your Website',
                'This is a message from Django',
                os.getenv('EHU'),
                [os.getenv('EHU')],
                fail_silently=False,
            )
            return HttpResponse('Email sent.')
    else:
        return render(request, 'bulletin.html')
