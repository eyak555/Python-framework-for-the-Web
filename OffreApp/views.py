from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import OffreForm
from .models import Offre


class ListOffre(ListView):
    model = Offre
    template_name = 'Offre/list.html'
    context_object_name = 'offres'
    queryset = Offre.objects.select_related('Entreprise', 'Vehicule', 'expedition')


class DetailOffre(DetailView):
    model = Offre
    template_name = 'Offre/details.html'
    context_object_name = 'offre'


class CreateOffre(LoginRequiredMixin, CreateView):
    model = Offre
    template_name = 'Offre/forms.html'
    form_class = OffreForm
    success_url = reverse_lazy('offre-list')


class UpdateOffre(LoginRequiredMixin, UpdateView):
    model = Offre
    template_name = 'Offre/forms.html'
    form_class = OffreForm
    success_url = reverse_lazy('offre-list')


class DeleteOffre(LoginRequiredMixin, DeleteView):
    model = Offre
    template_name = 'Offre/delete_confirmation.html'
    success_url = reverse_lazy('offre-list')
