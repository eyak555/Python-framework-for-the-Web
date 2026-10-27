from django.shortcuts import get_object_or_404, redirect, render
from django.http import HttpResponse
from .models import Expedition

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
