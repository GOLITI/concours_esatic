from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView, DetailView
from django.urls import reverse_lazy
from django.contrib import messages
from django.template.loader import render_to_string, get_template
from django.http import HttpResponse
from django.conf import settings
import os
from weasyprint import HTML, CSS
from io import BytesIO
from .models import Candidat, Concours
from .forms import InscriptionForm


class AccueilView(ListView):
    model = Concours
    template_name = 'inscriptions/index.html'
    context_object_name = 'concours'


class InscriptionView(CreateView):
    model = Candidat
    form_class = InscriptionForm
    template_name = 'inscriptions/inscription.html'
    success_url = reverse_lazy('confirmation')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, "Votre inscription a été enregistrée avec succès!")
        return response


class ConfirmationView(DetailView):
    model = Candidat
    template_name = 'inscriptions/confirmation.html'
    context_object_name = 'candidat'
    
    def get_object(self):
        return Candidat.objects.latest('date_inscription')


def generate_pdf(request, pk):
    # Récupérer les données du candidat
    candidat = Candidat.objects.get(pk=pk)
    
    # Préparer le contexte pour le template
    context = {'candidat': candidat}
    
    # Générer le HTML à partir du template PDF optimisé
    html_string = render_to_string('inscriptions/pdf_template.html', context)
    
    # Création d'un fichier temporaire pour stocker le PDF
    result = BytesIO()
    
    # Définir les polices si nécessaire
    font_config = {
        'Montserrat': {
            'normal': os.path.join(settings.STATIC_ROOT, 'fonts/Montserrat-Regular.ttf'),
            'bold': os.path.join(settings.STATIC_ROOT, 'fonts/Montserrat-Bold.ttf'),
            'italic': os.path.join(settings.STATIC_ROOT, 'fonts/Montserrat-Italic.ttf'),
            'bold_italic': os.path.join(settings.STATIC_ROOT, 'fonts/Montserrat-BoldItalic.ttf'),
        },
        'DejaVu Sans': {
            'normal': os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSans.ttf'),
            'bold': os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSans-Bold.ttf'),
        }
    }
    
    # Assurer que le répertoire des polices existe
    os.makedirs(os.path.join(settings.STATIC_ROOT, 'fonts'), exist_ok=True)
    
    # CSS supplémentaire pour la mise en page PDF
    css_string = '''
        @page {
            margin: 2cm 1.5cm;
            @top-center {
                content: "";
                height: 5mm;
                background-color: #037f8c;
            }
            @bottom-center {
                content: "Page " counter(page) " sur " counter(pages);
                font-size: 9pt;
                color: #666;
                padding-top: 3mm;
                border-top: 0.5pt solid #ddd;
            }
        }
        
        /* Assurer que les polices sont disponibles */
        @font-face {
            font-family: 'DejaVu Sans';
            src: url('%s');
            font-weight: normal;
            font-style: normal;
        }
    ''' % os.path.join(settings.STATIC_ROOT, 'fonts/DejaVuSans.ttf')
    
    # Base URL pour les ressources statiques
    base_url = request.build_absolute_uri('/')
    
    # Génération du PDF avec WeasyPrint
    html = HTML(string=html_string, base_url=base_url)
    css = CSS(string=css_string)
    
    # Créer le PDF avec les feuilles de style
    html.write_pdf(
        result,
        stylesheets=[css],
        presentational_hints=True,
        optimize_size=('fonts', 'images')
    )
    
    # Préparation de la réponse HTTP
    response = HttpResponse(result.getvalue(), content_type='application/pdf')
    filename = f"ESATIC_Inscription_{candidat.numero_inscription}.pdf"
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    return response