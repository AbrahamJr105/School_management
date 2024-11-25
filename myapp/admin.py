from django.contrib import admin

from .models import Filiere, Nationalite, Sport, Note, Etudiant, Module

# Register your models here.
admin.site.register(Filiere)
admin.site.register(Nationalite)
admin.site.register(Sport)
admin.site.register(Note)
admin.site.register(Module)
class EtudiantAdmin(admin.ModelAdmin):
    search_fields  = ['id',]
admin.site.register(Etudiant, EtudiantAdmin)
admin.site.site_header= 'Admin Panel'
admin.site.site_title= 'Admin Panel'