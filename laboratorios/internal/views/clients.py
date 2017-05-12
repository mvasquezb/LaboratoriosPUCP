from django.shortcuts import render
from django.http import HttpResponse
from internal import models


def index(request):
    return HttpResponse("Lista de clientes")


def create(request):
    if request.method == 'POST':
        name = request.POST.get('fname')
        if name:
            client = models.Client.objects.create(name=name)

    context = {}
    template = 'internal/clients.html'
    return render(request, template, context)
