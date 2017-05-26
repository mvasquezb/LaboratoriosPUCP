from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse


def index(request):
    return render(request, 'internal/request/index.html')


def create(request):
    context = {}

    return render(request, 'internal/request/create.html', context)


def store(request):
    context = {'message': 'Solicitud creada exitosamente'}

    return render(request, 'internal/request/index.html', context)
