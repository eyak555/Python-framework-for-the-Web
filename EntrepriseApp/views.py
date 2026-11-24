import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from OffreApp.models import Offre

from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

from .forms import EntrepriseForm, ProfileForm, RegisterForm


class ListEntreprise(ListView):
    model = Entreprise
    template_name = 'Entreprise/list.html'
    context_object_name = 'entreprises'


class DetailEntreprise(DetailView):
    model = Entreprise
    template_name = 'Entreprise/details.html'
    context_object_name = 'entreprise'


class CreateEntreprise(LoginRequiredMixin, CreateView):
    model = Entreprise
    template_name = 'Entreprise/forms.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('entreprise-list')


class UpdateEntreprise(LoginRequiredMixin, UpdateView):
    model = Entreprise
    template_name = 'Entreprise/forms.html'
    form_class = EntrepriseForm
    success_url = reverse_lazy('entreprise-list')


class DeleteEntreprise(LoginRequiredMixin, DeleteView):
    model = Entreprise
    template_name = 'Entreprise/delete_confirmation.html'
    success_url = reverse_lazy('entreprise-list')


@login_required
def profile(request):
    return render(request, 'profile/details.html', {'profile_user': request.user})


@login_required
def profile_edit(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == 'POST' and form.is_valid():
        form.save()
        return redirect('profile')

    return render(request, 'profile/forms.html', {'form': form})


@login_required
@require_http_methods(['GET', 'POST'])
def profile_delete(request):
    if request.method == 'POST':
        request.user.delete()
        logout(request)
        return redirect('project-home')

    return render(request, 'profile/delete_confirmation.html')


@staff_member_required
def health_check_view(request):
    
    now = timezone.now()
    sept_jours_avant = now - datetime.timedelta(days=7)

    # 1. Offres orphelines (en_attente ou acceptee dont l'expédition n'est plus publiee/attribuee)
    offres_orphelines = Offre.objects.filter(
        status__in=['en_attente', 'acceptee']
    ).exclude(
        expedition__status__in=['publiee', 'attribuee']
    ).select_related('expedition', 'Entreprise')

    # 2. Expéditions bloquées (publiees depuis plus de 7 jours)
    expeditions_bloquees = Expedition.objects.filter(
        status='publiee',
        created_at__lt=sept_jours_avant
    ).select_related('entreprise')

    # 3. Transporteurs sans flotte (entreprises de type 'T' sans véhicule rattaché)
    transporteurs_sans_flotte = (
        Entreprise.objects
        .filter(type_entreprise='T')
        .annotate(nb_vehicules=Count('entreprises_vehicules'))
        .filter(nb_vehicules=0)
    )

    # 4. Incohérence de disponibilité (véhicule disponible=True mais affecté à une offre acceptee)
    vehicules_incoherents = (
        Vehicule.objects
        .filter(disponibilite=True, vehicules_offres__status='acceptee')
        .distinct()
        .select_related('Entreprise')
    )

    # 5. Doublons de proposition (entreprise avec >1 offre en_attente pour la même expédition)
    doublons_propositions = (
        Offre.objects
        .filter(status='en_attente')
        .values('Entreprise__raison_sociale', 'expedition__reference')
        .annotate(nb_offres=Count('id'))
        .filter(nb_offres__gt=1)
    )

    total_anomalies = (
        offres_orphelines.count()
        + expeditions_bloquees.count()
        + transporteurs_sans_flotte.count()
        + vehicules_incoherents.count()
        + doublons_propositions.count()
    )

    context = {
        'title': "Contrôle d'intégrité métier",
        'site_header': getattr(request, 'site_header', "transconnect - Administration"),
        'has_permission': True,
        'offres_orphelines': offres_orphelines,
        'expeditions_bloquees': expeditions_bloquees,
        'transporteurs_sans_flotte': transporteurs_sans_flotte,
        'vehicules_incoherents': vehicules_incoherents,
        'doublons_propositions': doublons_propositions,
        'total_anomalies': total_anomalies,
        'now': now,
    }

    return render(request, 'admin/health_check.html', context)


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirige vers la page de connexion après l'inscription réussie
    else:
        form = RegisterForm()
    return render(request, 'register.html', {'form': form})
