from django.shortcuts import render
from django.http import HttpResponse
from internal import models
from internal.models import Client

def index(request):
    dict = {}
    template = 'internal/clients.html'
    return render(request, template, dict)


def create_new_client(request):
    if request.method == 'POST':
        name = request.POST.get('fname')
        client = models.Client.objects.create(name=name)
    else:
        pass
    return HttpResponse("Cliente creado con exito")