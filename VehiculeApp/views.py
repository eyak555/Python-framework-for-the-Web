from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import VehiculeForm
from .models import Vehicule


class ListVehicule(ListView):
    model = Vehicule
    template_name = 'Vehicule/list.html'
    context_object_name = 'vehicules'


class DetailVehicule(DetailView):
    model = Vehicule
    template_name = 'Vehicule/details.html'
    context_object_name = 'vehicule'


class CreateVehicule(CreateView):
    model = Vehicule
    template_name = 'Vehicule/forms.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicule-list')


class UpdateVehicule(UpdateView):
    model = Vehicule
    template_name = 'Vehicule/forms.html'
    form_class = VehiculeForm
    success_url = reverse_lazy('vehicule-list')


class DeleteVehicule(DeleteView):
    model = Vehicule
    template_name = 'Vehicule/delete_confirmation.html'
    success_url = reverse_lazy('vehicule-list')
