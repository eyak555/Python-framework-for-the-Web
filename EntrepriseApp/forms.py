from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

from .models import Entreprise


class EntrepriseForm(forms.ModelForm):
    class Meta:
        model = Entreprise
        exclude = ('creation_date', 'update_date')


class RegisterForm(UserCreationForm):
    role = forms.ChoiceField(choices=(
        ('C', 'Chargeur'),
        ('T', 'Transporteur'),
    ))

    class Meta (UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields + (
            'first_name',
            'last_name',
            'email',
            'role',
            'telephone',
        )

class ProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ('username', 'first_name', 'last_name', 'email', 'telephone')