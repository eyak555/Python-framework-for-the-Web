from django.db import models
from EntrepriseApp.models import Entreprise
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError

# Create your models here.
class Expedition(models.Model):
    reference = models.CharField(max_length=100, unique=True)
    ville_depart = models.CharField(max_length=100)
    ville_arrivee = models.CharField(max_length=100)
    poids = models.DecimalField(max_digits=10, decimal_places=2)
    MinValueValidator(0.1, "Le poids doit être supérieur à 0")

    date_souhaitee = models.DateField()
    description = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=20, 
    choices=[('en_attente', 'En attente'),
                ('publiee', 'Publiée'),
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
    )
    def clean(self):
        super().clean()
        if self.entreprise_id and self.entreprise.type_entreprise != 'Chargeur':
            raise ValidationError({"entreprise": "entreprise : une expedition ne peut etre cree que par un chargeur."})


    @classmethod
    #EXP_26_12569(auto incremente)

    def _generate_reference(cls):
        annee = timezone.now().strftime('%Y') # recupere l'année en cours
        prefixe =f"EXP_{annee}_"
        dernier = (
           # !! cls.ojjects.all()) select * expedition
            cls.objects.filter(reference__startswith=prefixe)
            .order_by('reference') #par defaut ascendant -reference descendant
            .last() #recupere la derniere expedition
        )
        #ajout de 1 au dernier compteur
        compteur = (int(dernier.reference.split[-5]) + 1 if dernier 
        else 1 # si rien nexiste, on commence à 1
        )
        if compteur > 99999:
            raise ValidationError("limit exceeded")

        return f"{prefixe}{compteur:05d}" #formatage du compteur sur 5 chiffres avec des zéros devant


    def save(self, *args, **kwargs): # ki manarch 9adeh andi men parametre (*args, **kwargs) args : attributs, kwargs : les fonctions
        if not self.reference:
            self.reference = self.generate_reference()

        #fct appele pour appliquer les validateurs
        self.full.clean() #valide les champs avant de sauvegarder
        super().save(*args, **kwargs)
        
        