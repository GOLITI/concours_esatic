from django.contrib import admin
from .models import Concours, Candidat

class CandidatAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'concours', 'numero_inscription', 'date_inscription')
    list_filter = ('concours', 'niveau_etude')
    search_fields = ('nom', 'prenom', 'numero_inscription', 'email')
    readonly_fields = ('date_inscription', 'numero_inscription')
    ordering = ('-date_inscription',)

admin.site.register(Concours)
admin.site.register(Candidat, CandidatAdmin)