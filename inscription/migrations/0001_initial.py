# Generated by Django 5.2 on 2025-04-30 15:22

import django.core.validators
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Concours',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('date_limite', models.DateField()),
                ('frais_inscription', models.DecimalField(decimal_places=2, max_digits=10)),
            ],
        ),
        migrations.CreateModel(
            name='Candidat',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('prenom', models.CharField(max_length=100)),
                ('date_naissance', models.DateField()),
                ('lieu_naissance', models.CharField(max_length=100)),
                ('nationalite', models.CharField(max_length=100)),
                ('niveau_etude', models.CharField(choices=[('BAC', 'Baccalauréat'), ('BAC+1', 'Bac+1'), ('BAC+2', 'Bac+2'), ('BAC+3', 'Bac+3'), ('BAC+4', 'Bac+4'), ('BAC+5', 'Bac+5')], max_length=20)),
                ('etablissement_origine', models.CharField(max_length=200)),
                ('telephone', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('extrait_naissance', models.FileField(upload_to='extraits_naissance/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('certificat', models.FileField(upload_to='certificats/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('lettre_motivation', models.FileField(upload_to='lettres_motivation/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'doc', 'docx'])])),
                ('diplome', models.FileField(upload_to='diplomes/', validators=[django.core.validators.FileExtensionValidator(['pdf', 'jpg', 'jpeg', 'png'])])),
                ('photo', models.ImageField(upload_to='photos/', validators=[django.core.validators.FileExtensionValidator(['jpg', 'jpeg', 'png'])])),
                ('date_inscription', models.DateTimeField(auto_now_add=True)),
                ('numero_inscription', models.CharField(blank=True, max_length=20, unique=True)),
                ('concours', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='inscription.concours')),
            ],
        ),
    ]
