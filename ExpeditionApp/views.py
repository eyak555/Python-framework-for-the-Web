from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView
from .models import Expedition
from .forms import ExpeditionForm

# Create your views here.
def home (request):
    return HttpResponse("<h1>Welcome to the Expedition App</h1>")

def welcome(request, name):
    return HttpResponse(f"hello {name}")

def listExpeditions(request):
    liste = Expedition.objects.all()
    return render(request, 'expedition/list.html', {'list': liste}) 

def details(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    return render(request, 'expedition/details.html', {'expedition': expedition})


def delete_expedition(request, pk):
    expedition = get_object_or_404(Expedition, pk=pk)
    if request.method == 'POST':
        expedition.delete()
        return redirect('list')

    return render(request, 'expedition/delete_confirmation.html', {
        'expedition': expedition
    })
class ListExpedition(ListView):
    model=Expedition
    template_name='Expedition/list.html'
    context_object_name='list'

class DetailExpedition(DetailView):
    model=Expedition
    template_name='Expedition/details.html'
    context_object_name='expedition'

class DeleteExpedition(DeleteView):
    model=Expedition
    template_name='Expedition/delete_confirmation.html'
    success_url=reverse_lazy('listclass')

class CreateExpedition(CreateView):
    model=Expedition
    template_name='Expedition/forms.html'
    form_class=ExpeditionForm
    success_url=reverse_lazy('listclass')

class UpdateExpedition(UpdateView):
    model = Expedition
    template_name = 'Expedition/forms.html'
    form_class = ExpeditionForm
    success_url = reverse_lazy('listclass')
