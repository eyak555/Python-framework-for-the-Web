from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.
class Expedition(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, 
    choices=[('en_attente', 'En attente'),
                ('en_cours', 'En cours'),   
                ('terminee', 'Terminée'),
                ('annulee', 'Annulée'),     
    ], default='en_attente')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    entreprise = models.ForeignKey(
        Entreprise,
        on_delete=models.CASCADE,
        related_name='entreprises',
        blank=True,
        null=True,
    )