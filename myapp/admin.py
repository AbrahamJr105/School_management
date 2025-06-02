from django.contrib import admin

from .models import Filiere, Nationalite, Sport, Note, Etudiant, Module, Enseignant

# Register your models here.
admin.site.register(Filiere)
admin.site.register(Nationalite)
admin.site.register(Sport)
admin.site.register(Module)
admin.site.register(Enseignant)
class EtudiantAdmin(admin.ModelAdmin):
    search_fields  = ['id',]
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.site_header= 'Admin Panel'
admin.site.site_title= 'Admin Panel'

class NoteAdmin(admin.ModelAdmin):
    list_display = ('etudiant', 'module', 'filiere', 'note')
    search_fields = ('etudiant__nom_pre', 'module__name', 'filiere__filiere_inscription')
    list_filter = ('filiere', 'module')

admin.site.register(Note, NoteAdmin)