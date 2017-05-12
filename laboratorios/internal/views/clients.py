from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from internal import models


def index(request, template = 'internal/clients/list.html',extra_context=None):
    clientes = models.Client.objects.all()
    context = {'clientes':clientes}
    return render (request,template,context)


def create(request):
    if request.method == 'POST':
        name = request.POST.get('fname')
        if name:
            client = models.Client.objects.create(name=name)

    context = {}
    template = 'internal/clients/create.html'
    return render(request, template, context)


def edit(request, client_id):
    client = get_object_or_404(models.Client, pk=client_id)
    context = {'client': client}
    return render(request, 'internal/clients/edit.html', context)


def update(request, client_id):
    client = get_object_or_404(models.Client, pk=client_id)
    client.name = request.POST.get('fname')
    client.save()
    context = {'message': 'Client edited successfully'}
    return render(request, 'internal/index.html', context)
