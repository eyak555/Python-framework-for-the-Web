from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator, RegexValidator
from django.utils import timezone
# Create your models here.


#validators
def validate_email(value):
    if not value:
        raise ValidationError("L'adresse e-mail est obligatoire.")
    if not value.endswith('@gmail.com'):
        raise ValidationError("L'adresse e-mail doit se terminer par '@gmail.com'.")

matricule_fiscale_validator = RegexValidator(
    regex=r'^\d{7}[/ -]?[A-Za-z][/ -]?[ABDNPEabdnpe][/ -]?[MPCNEmpcne][/ -]?\d{3}$', message="Le format est errone'.")



class utilisateur(AbstractUser):
    user_id = models.CharField(primary_key=True, max_length=8, unique=True)
    email = models.EmailField(unique=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    role = models.CharField(max_length=20, 
    choices=[('admin', 'Admin'),   
    ('C', 'Chargeur'),
    ('T', 'Transporteur'),
    ], default='C')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    @classmethod
    def generate_user_id(cls):
        annee = timezone.now().strftime('%y')
        prefixe = f"{annee}user"

        dernier = (
            cls.objects
            .filter(user_id__startswith=prefixe)
            .order_by('user_id')
            .last()
        )

        compteur = (
            int(dernier.user_id[-2:]) + 1 if dernier
            else 0
        )

        if compteur > 99:
            raise ValidationError("Limite de 99 user.")

        return f"{prefixe}{compteur:02d}"

    def save(self, *args, **kwargs):
        if not self.user_id:
            self.user_id = self.generate_user_id()

        super().save(*args, **kwargs)



class Entreprise(models.Model):
    raison_sociale = models.CharField(max_length=200, blank=False, null=False)
    matricule_fiscale = models.CharField(max_length=17, unique=True, blank=False, null=False)
    adresse = models.TextField()
    MinLengthValidator(20,"l'adresse doit contenir au moins 20 caractères")
    MaxLengthValidator(400,"l'adresse doit contenir au maximum 200 caractères")
    type_entreprise = models.CharField(max_length=100, 
    choices=[
        ('C', 'Chargeur'),
        ('T', 'Transporteur'),
        ('A', 'Autre'),
    ])
    creation_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    gerant = models.OneToOneField(utilisateur, on_delete=models.CASCADE, 
    related_name='entreprise')
       
  
