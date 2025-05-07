from django.db import models
from django.core.validators import FileExtensionValidator

class Concours(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField()
    date_limite = models.DateField()
    frais_inscription = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __str__(self):
        return self.nom

class Candidat(models.Model):
    NIVEAU_CHOICES = [
        ('BAC', 'Baccalauréat'),
        ('BAC+1', 'Bac+1'),
        ('BAC+2', 'Bac+2'),
        ('BAC+3', 'Bac+3'),
        ('BAC+4', 'Bac+4'),
        ('BAC+5', 'Bac+5'),
    ]
    
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    nationalite = models.CharField(max_length=100)
    niveau_etude = models.CharField(max_length=20, choices=NIVEAU_CHOICES)
    etablissement_origine = models.CharField(max_length=200)
    telephone = models.CharField(max_length=20)
    email = models.EmailField()
    concours = models.ForeignKey(Concours, on_delete=models.CASCADE)
    
    # Fichiers
    extrait_naissance = models.FileField(
        upload_to='extraits_naissance/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    certificat = models.FileField(
        upload_to='certificats/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    lettre_motivation = models.FileField(
        upload_to='lettres_motivation/',
        validators=[FileExtensionValidator(['pdf', 'doc', 'docx'])]
    )
    diplome = models.FileField(
        upload_to='diplomes/',
        validators=[FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])]
    )
    photo = models.ImageField(
        upload_to='photos/',
        validators=[FileExtensionValidator(['jpg', 'jpeg', 'png'])]
    )
    
    date_inscription = models.DateTimeField(auto_now_add=True)
    numero_inscription = models.CharField(max_length=20, unique=True, blank=True)
    
    def save(self, *args, **kwargs):
        if not self.numero_inscription:
            last_id = Candidat.objects.all().count() + 1
            self.numero_inscription = f"ESATIC-{self.concours.nom[:3].upper()}-{last_id:05d}"
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.nom} {self.prenom} - {self.numero_inscription}"