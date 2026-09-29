from django.db import models
from EntrepriseApp.models import Entreprise

# Create your models here.
class Offre(models.Model):
    prix = models.DecimalField(max_digits=10, decimal_places=2)
    delai_jours = models.IntegerField()
    status = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('acceptee', 'Acceptée'), ('refusee', 'Refusée')], default='en_attente')
    date_proposition = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    Entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE,
        related_name='entreprises_offres',
        blank=True,
        null=True,)

    Vehicule = models.ForeignKey(
        'VehiculeApp.Vehicule', on_delete=models.CASCADE,
        related_name='vehicules_offres',
        blank=True,
        null=True,)

    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition', on_delete=models.CASCADE,
        related_name='expeditions_offres',
        blank=True,     
    null=True,)

    