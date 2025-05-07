from django.urls import path
from . import views

urlpatterns = [
    path('', views.AccueilView.as_view(), name='accueil'),
    path('inscription/', views.InscriptionView.as_view(), name='inscription'),
    path('confirmation/', views.ConfirmationView.as_view(), name='confirmation'),
    path('pdf/<int:pk>/', views.generate_pdf, name='generate_pdf'),
]