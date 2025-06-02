import os
import json
import base64
from django.contrib import auth, messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_not_required
from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.db.models import Sum, F
from django.views.decorators.csrf import csrf_exempt
from dotenv import load_dotenv

from .forms import loginform, filierepv
from .models import Etudiant, Note, Module, Enseignant, Filiere

load_dotenv()


@login_not_required
def logout(request):
    """Handle user logout."""
    auth.logout(request)
    messages.success(request, "Vous avez été déconnecté avec succès.")
    return redirect('login')


@login_not_required
def login(request):
    """Handle user login."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        
        if not email or not password:
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'accounts/login.html', {'form': loginform()})
        
        user = authenticate(username=email, password=password)
        if user is not None:
            auth.login(request, user)
            if user.is_staff:
                messages.success(request, f"Bienvenue, {user.username}!")
                return redirect('menu')
            return redirect('bulletin')
        else:
            messages.error(request, "Email ou mot de passe incorrect.")
    
    form = loginform()
    return render(request, 'accounts/login.html', {'form': form})


@login_not_required
def register(request):
    """Handle user registration."""
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if not all([email, password, role]):
            messages.error(request, "Veuillez remplir tous les champs.")
            return render(request, 'accounts/register.html', {'form': loginform()})
        
        if User.objects.filter(username=email).exists():
            messages.error(request, "Un utilisateur avec cet email existe déjà.")
            return render(request, 'accounts/register.html', {'form': loginform()})
        
        try:
            user = User.objects.create_user(username=email, email=email, password=password)
            user.is_superuser = role == 'admin'
            user.is_staff = role == 'admin'
            user.save()
            messages.success(request, "Compte créé avec succès! Vous pouvez maintenant vous connecter.")
            return redirect('login')
        except Exception as e:
            messages.error(request, "Erreur lors de la création du compte.")
    
    form = loginform()
    return render(request, 'accounts/register.html', {'form': form})


@staff_member_required(login_url='/login/')
def menu(request):
    """Display main dashboard menu."""
    return render(request, 'myapp/menu.html')


@staff_member_required(login_url='/login/')
def pv(request):
    """
    Generate academic transcripts (PV) for programs.
    Displays student grades, pass/fail statistics, and provides email/print functionality.
    """
    if request.method == 'POST':
        if 'afficher' in request.POST:
            try:
                filiere_id = request.POST.get('filiere')
                if not filiere_id:
                    messages.error(request, "Please select a program.")
                    form = filierepv()
                    return render(request, 'myapp/pv.html', {'form': form})
                
                filiere = Filiere.objects.get(pk=filiere_id)
                etudiants = Etudiant.objects.filter(filiere=filiere)
                
                if not etudiants.exists():
                    messages.warning(request, f"No students found in {filiere.filiere_inscription} program.")
                    form = filierepv()
                    return render(request, 'myapp/pv.html', {'form': form})
                
                student_grades = []
                passinggrades = 0
                failinggrades = 0
                
                for etudiant in etudiants:
                    # Calculate weighted average grade
                    weighted_sum_of_notes = Note.objects.filter(etudiant=etudiant).annotate(
                        weighted_note=F('note') * F('module__coefficient')
                    ).aggregate(total_weighted=Sum('weighted_note'))['total_weighted'] or 0

                    sum_of_coefficients = Module.objects.filter(filiere=etudiant.filiere).aggregate(
                        total_coefficient=Sum('coefficient')
                    )['total_coefficient'] or 1

                    average_grade = weighted_sum_of_notes / sum_of_coefficients if sum_of_coefficients > 0 else 0

                    student_grades.append({
                        'student': etudiant,
                        'average_grade': average_grade
                    })
                    
                    if average_grade >= 10:
                        passinggrades += 1
                    else:
                        failinggrades += 1
                
                # Sort by average grade (highest first)
                student_grades.sort(key=lambda x: x['average_grade'], reverse=True)
                
                # Store HTML content for email
                request.session['html_content'] = render_to_string(
                    "myapp/html_content.html", 
                    {
                        'student_grades': student_grades, 
                        'filiere': filiere,
                        'passinggrades': passinggrades,
                        'failinggrades': failinggrades
                    }
                )
                
                form = filierepv()
                messages.success(request, f"Transcript generated for {filiere.filiere_inscription} with {len(student_grades)} students.")
                
                return render(request, 'myapp/pv.html', {
                    'filiere': filiere, 
                    'student_grades': student_grades, 
                    'passinggrades': passinggrades,
                    'failinggrades': failinggrades, 
                    'form': form
                })
                
            except Filiere.DoesNotExist:
                messages.error(request, "Selected program not found.")
                form = filierepv()
                return render(request, 'myapp/pv.html', {'form': form})
            except Exception as e:
                messages.error(request, f"An error occurred while generating the transcript: {str(e)}")
                form = filierepv()
                return render(request, 'myapp/pv.html', {'form': form})
        
        elif 'emailChart' in request.POST:
            try:
                image_data = request.session.get('image')
                if not image_data:
                    messages.error(request, "No chart image found. Please generate a transcript first.")
                    return redirect('pv')
                
                image = base64.b64decode(image_data)
                
                email = EmailMessage(
                    'Academic Statistics Chart',
                    'Please find attached the academic statistics chart for your program.',
                    os.getenv('EMAIL_FROM', 'noreply@school.edu'),
                    [os.getenv('EMAIL_TO', 'admin@school.edu')],
                )
                email.content_subtype = "html"
                email.attach("academic_chart.png", image, "image/png")
                email.send()
                
                messages.success(request, "Chart email sent successfully.")
                return redirect('pv')
                
            except Exception as e:
                messages.error(request, f"Failed to send chart email: {str(e)}")
                return redirect('pv')
        
        elif 'email' in request.POST:
            try:
                html_content = request.session.get('html_content')
                if not html_content:
                    messages.error(request, "No transcript data found. Please generate a transcript first.")
                    return redirect('pv')
                
                email = EmailMessage(
                    'Academic Transcript Report',
                    html_content,
                    os.getenv('EMAIL_FROM', 'noreply@school.edu'),
                    [os.getenv('EMAIL_TO', 'admin@school.edu')],
                )
                email.content_subtype = "html"
                email.send()
                
                messages.success(request, "Transcript email sent successfully.")
                return redirect('pv')
                
            except Exception as e:
                messages.error(request, f"Failed to send transcript email: {str(e)}")
                return redirect('pv')
    
    # GET request
    form = filierepv()
    return render(request, 'myapp/pv.html', {'form': form})

@staff_member_required(login_url='/login/')
def statistique(request):
    """
    Display student statistics and demographics.
    Shows gender distribution and enrollment analytics.
    """
    try:
        all_students = Etudiant.objects.all().count()
        
        if all_students == 0:
            messages.info(request, "No students found in the database.")
            return render(request, 'myapp/statistique.html', {
                'male': 0, 
                'female': 0, 
                'all': 0
            })
        
        male_count = Etudiant.objects.filter(civilite="Mr").count()
        female_count = Etudiant.objects.filter(civilite__in=["Mrs", "Ms"]).count()
        
        # Additional statistics could be added here
        context = {
            'male': male_count, 
            'female': female_count, 
            'all': all_students,
            'male_percentage': (male_count / all_students * 100) if all_students > 0 else 0,
            'female_percentage': (female_count / all_students * 100) if all_students > 0 else 0,
        }
        
        return render(request, 'myapp/statistique.html', context)
        
    except Exception as e:
        messages.error(request, f"An error occurred while loading statistics: {str(e)}")
        return render(request, 'myapp/statistique.html', {
            'male': 0, 
            'female': 0, 
            'all': 0
        })


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
            notes = Note.objects.filter(etudiant_id=idetu)
            statistiques = notes.aggregate(
                SommeCoefficient=Sum(F('module__coefficient')),
                SommeCoiNotes=Sum(F('module__coefficient') * F('note')),
                moyenne=Sum(F('module__coefficient') * F('note')) / Sum('module__coefficient')
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

@csrf_exempt
def save_chart_image(request):
    """
    Save chart image from client-side canvas to session for email functionality.
    """
    if request.method == "POST":
        try:
            import json
            data = json.loads(request.body)
            chart_image = data.get("chart_image")

            if chart_image:
                # Extract base64 image data
                if ';base64,' in chart_image:
                    format, imgstr = chart_image.split(';base64,')
                    request.session['image'] = imgstr
                    return JsonResponse({'success': True, 'message': 'Chart image saved successfully'})
                else:
                    return JsonResponse({'success': False, 'error': 'Invalid image format'}, status=400)
            else:
                return JsonResponse({'success': False, 'error': 'No image data provided'}, status=400)
                
        except json.JSONDecodeError:
            return JsonResponse({'success': False, 'error': 'Invalid JSON data'}, status=400)
        except Exception as e:
            return JsonResponse({'success': False, 'error': f'Server error: {str(e)}'}, status=500)

    return JsonResponse({'success': False, 'error': 'Only POST method allowed'}, status=405)
