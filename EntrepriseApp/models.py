from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator
from django.core.validators import MaxLengthValidator, RegexValidator
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
       
  
