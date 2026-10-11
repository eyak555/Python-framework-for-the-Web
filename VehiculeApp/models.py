from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Vehicule(models.Model):
    immatriculation = models.CharField(max_length=20, unique=True)
    type_vehicule = models.CharField(max_length=50, choices=[('camion', 'Camion'), ('voiture', 'Voiture'), ('moto', 'Moto')])
    capacite = models.PositiveIntegerField(validators=[MinValueValidator(1, "La capacité doit être supérieure à 0")])
    disponibilite = models.BooleanField(default=True)
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=[('en_service', 'En service'), ('hors_service', 'Hors service')], default='en_service')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    Entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE,
        related_name='entreprises_vehicules',
        )

    Offre = models.ForeignKey(
        'OffreApp.Offre', on_delete=models.CASCADE,
        related_name='offres_vehicules',
        )

    def clean(self):
        super().clean()

        if self.Entreprise_id and self.Entreprise.type_entreprise != 'T':
            raise ValidationError({
                'Entreprise': 'L’entreprise doit être de type transporteur.'
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
