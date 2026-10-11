from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Offre(models.Model):
    prix = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0.01, "Le prix doit être supérieur à 0")],
    )
    delai_jours = models.IntegerField(
        validators=[MinValueValidator(1, "Le délai doit être supérieur ou égal à 1")]
    )
    status = models.CharField(max_length=20, choices=[('en_attente', 'En attente'), ('acceptee', 'Acceptée'), ('refusee', 'Refusée')], default='en_attente')
    date_proposition = models.DateTimeField(auto_now_add=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    Entreprise = models.ForeignKey(
        Entreprise, on_delete=models.CASCADE,
        related_name='entreprises_offres',
        )

    Vehicule = models.ForeignKey(
        'VehiculeApp.Vehicule', on_delete=models.CASCADE,
        related_name='vehicules_offres',
        )

    expedition = models.ForeignKey(
        'ExpeditionApp.Expedition', on_delete=models.CASCADE,
        related_name='expeditions_offres',
        )

    def clean(self):
        super().clean()

        if self.Entreprise_id and self.Entreprise.type_entreprise != 'T':
            raise ValidationError({
                'Entreprise': 'Une offre ne peut être créée que par transporteur.'
            })

        if self.expedition_id and self.expedition.status != 'publiee':
            raise ValidationError({
                'expedition': (
                    'Une offre ne peut être créée que pour une expédition publiée.'
                )
            })

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)
    