from django.contrib import auth
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from dotenv import load_dotenv
from .forms import EtudiantForm, RechercheForm, loginform, EnseignantForm, filierepv

load_dotenv()
def logout(request):
    auth.logout(request)
    return redirect('login')
@login_not_required
def login(request):
    if request.method == 'POST':
            user = authenticate(username=request.POST['email'],password=request.POST['password'])
            if user is not None:
                auth.login(request, user)
                request.session['user_email'] = user.get_username()
                return redirect('menu')
            else:
                return HttpResponse("Wrong credentials")
    else:
        form = loginform()
    return render(request, 'accounts/login.html', {'form': form})
@login_not_required
def register(request):
    if request.method == 'POST':
        form = loginform(request.POST)
        if form.is_valid():
            user=User.objects.create_user(request.POST['email'],None, request.POST['password'])
            user.is_staff = False if request.POST['role'] == 'user' else True
            user.save()
            return redirect('login')
    else:
        form = loginform()
    return render(request, 'accounts/register.html', {'form': form})
@staff_member_required
def menu(request):
    return render(request, 'myapp/menu.html')
@staff_member_required
def etudiant_form(request):
    if request.method == 'POST':
        if 'Enregistrer' in request.POST:
            form = EtudiantForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Saved.')
            else:
                return render(request, 'myapp/etudiant_form.html', {'form': form})
        elif 'rechercher' in request.POST:
            search_form = RechercheForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['numero']
                try:
                    etudiant = Etudiant.objects.get(pk=search_id)
                    return render(request, 'myapp/etudiant_form.html', {'etudiant': etudiant})
                except Etudiant.DoesNotExist:
                    return HttpResponse("mf was not found")
            else:
                print(search_form.errors)
        elif 'supprimer' in request.POST:
            search_form = RechercheForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['numero']
                try:
                    etudiant = Etudiant.objects.get(pk=search_id)
                    etudiant.delete()
                    return redirect('etudiant_form')
                except Etudiant.DoesNotExist:
                    error_message = "Etudiant introuvable."
                    return render(request, 'myapp/etudiant_form.html', {'error_message': error_message})
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
                return render(request, 'myapp/etudiant_form.html', {'error_message': error_message})
    else:
        form=EtudiantForm()
        search_form=RechercheForm()
        return render(request, 'myapp/etudiant_form.html', {"search_form":search_form, 'form': form})

def enseignant_form(request):
    if request.method == 'POST':
        if 'Enregistrer' in request.POST:
            form = EnseignantForm(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponse('Saved.')
            else:
                return render(request, 'myapp/enseignant_form.html', {'form': form})
        elif 'rechercher' in request.POST:
            search_form = RechercheForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['Numero']
                try:
                    enseignant = Enseignant.objects.get(pk=search_id)
                    return render(request, 'myapp/enseignant_form.html', {'enseignant': enseignant})
                except Enseignant.DoesNotExist:
                    return HttpResponse("Enseignant not found")
            else:
                print(search_form.errors)
        elif 'supprimer' in request.POST:
            search_form = RechercheForm(request.POST)
            if search_form.is_valid():
                search_id = search_form.cleaned_data['Numero']
                try:
                    enseignant = Enseignant.objects.get(pk=search_id)
                    enseignant.delete()
                    return redirect('enseignant_form')
                except Enseignant.DoesNotExist:
                    error_message = "Enseignant not found."
                    return render(request, 'myapp/enseignant_form.html', {'error_message': error_message})
        elif 'modifier' in request.POST:
            search_id = request.POST.get('Numero')
            try:
                enseignant = Enseignant.objects.get(pk=search_id)
                if search_id and request.POST:
                    form = EnseignantForm(request.POST, instance=enseignant)
                    if form.is_valid():
                        form.save()
                        return redirect('enseignant_form')
                    else:
                        print(form.errors)
            except Enseignant.DoesNotExist:
                error_message = "Enseignant not found."
                return render(request, 'myapp/enseignant_form.html', {'error_message': error_message})
    else:
        form=EnseignantForm()
        search_form=RechercheForm()
        return render(request, 'myapp/enseignant_form.html', {"search_form":search_form, 'form': form})
@staff_member_required
def pv(request):
    if request.method == 'POST':
        if 'afficher' in request.POST:
            filiere=request.POST.get('filiere')
            filiere=Filiere.objects.get(pk=filiere)
            etudiants = Etudiant.objects.filter(filiere=filiere)
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
            form = filierepv()
            request.session['html_content']=render_to_string("myapp/html_content.html", {'student_grades': student_grades, 'filiere':filiere})
            return render(request, 'myapp/pv.html',{'filiere': filiere, 'student_grades': student_grades, 'passinggrades': passinggrades,'failinggrades': failinggrades, 'form': form})
        if 'emailChart' in request.POST:
            image = request.session['image']
            image= base64.b64decode(image)
            # Retrieve the HTML content from the session
            email = EmailMessage(
                'Subject: Message from Your Website',
                'Here is the chart image:',
                os.getenv('EHU'),
                [os.getenv('EHU')],
            )
            email.content_subtype = "html"
            email.attach("chartImage", image, "image/png")  # Indicate that the email content is HTML
            email.send()

            return HttpResponse('Chart email sent.')
        elif 'email' in request.POST:
            html_content=request.session['html_content']
            email = EmailMessage(
                'Subject: Message from Your Website',
                html_content,
                os.getenv('EHU'),
                [os.getenv('EHU')],
            )
            email.content_subtype = "html"
            email.send()
            return HttpResponse('Email sent.')
    else:
        form=filierepv()
        return render(request, 'myapp/pv.html', {'form':form})
@staff_member_required
def statistique(request):
    all=Etudiant.objects.all().count()
    male = Etudiant.objects.filter(civilite="Monsieur").count()
    female = all-male
    return render(request, 'myapp/statistique.html', {'male': male, 'female': female, 'all': all})


from .models import Etudiant, Note, Module, Enseignant,Filiere

from django.template.loader import render_to_string
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.core.mail import EmailMessage
from django.db.models import Sum, F
import os

def bulletin_view(request):
    if request.method == 'POST':
        if 'bulletin' in request.POST:
            idetu = request.POST.get('num')
            etudiant = get_object_or_404(Etudiant, id=idetu)
            notes = Note.objects.filter(Etudiant_id=idetu)
            statistiques = notes.aggregate(
                SommeCoefficient=Sum(F('Module__coefficient')),
                SommeCoiNotes=Sum(F('Module__coefficient') * F('note')),
                moyenne=Sum(F('Module__coefficient') * F('note')) / Sum('Module__coefficient')
            )
            # Render the HTML content once and store it in the session
            request.session["html_content"]= render_to_string("myapp/html_content.html", {'etudiant': etudiant, 'notes': notes, 'statistiques': statistiques, })
          # Store rendered HTML in session
            return render(request, 'myapp/bulletin.html', {'etudiant': etudiant, 'notes': notes, 'statistiques': statistiques, })   # Render the bulletin in the browser

        elif 'email' in request.POST:
            html_content = request.session['html_content']
            # Retrieve the HTML content from the session
            email = EmailMessage(
                'Subject: Message from Your Website',
                html_content,
                os.getenv('EHU'),
                [os.getenv('EHU')],
            )
            email.content_subtype = "html"
            email.send()

            return HttpResponse('Email sent.')
    else:
        return render(request, 'myapp/bulletin.html')

import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt  # Skip CSRF for testing; use CSRF properly in production
def save_chart_image(request):
    if request.method == "POST":
        import json
        data = json.loads(request.body)
        chart_image = data.get("chart_image")

        if chart_image:
            # Decode Base64 to binary
            format, imgstr = chart_image.split(';base64,')
            request.session['image'] = imgstr
            # Save the file (optional)
            return JsonResponse({'success': True})

    return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)
