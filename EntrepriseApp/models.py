from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.
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
       
  
