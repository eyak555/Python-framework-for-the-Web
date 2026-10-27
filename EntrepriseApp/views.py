import datetime
from django.shortcuts import render
from django.utils import timezone
from django.db.models import Count
from django.contrib.admin.views.decorators import staff_member_required

from EntrepriseApp.models import Entreprise
from VehiculeApp.models import Vehicule
from ExpeditionApp.models import Expedition
from OffreApp.models import Offre


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
