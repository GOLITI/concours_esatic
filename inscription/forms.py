from django import forms
from .models import Candidat, Concours
from django.core.validators import FileExtensionValidator

class InscriptionForm(forms.ModelForm):
    concours = forms.ModelChoiceField(
        queryset=Concours.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Candidat
        fields = '__all__'
        exclude = ['date_inscription', 'numero_inscription']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'prenom': forms.TextInput(attrs={'class': 'form-control'}),
            'date_naissance': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'lieu_naissance': forms.TextInput(attrs={'class': 'form-control'}),
            'nationalite': forms.TextInput(attrs={'class': 'form-control'}),
            'niveau_etude': forms.Select(attrs={'class': 'form-control'}),
            'etablissement_origine': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'extrait_naissance': forms.FileInput(attrs={'class': 'form-control'}),
            'certificat': forms.FileInput(attrs={'class': 'form-control'}),
            'lettre_motivation': forms.FileInput(attrs={'class': 'form-control'}),
            'diplome': forms.FileInput(attrs={'class': 'form-control'}),
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if isinstance(field, forms.FileField):
                field.required = True