from django.shortcuts import render, get_object_or_404, redirect, reverse, HttpResponseRedirect
from django.http import HttpResponse

from internal.models import Request

def index(request):
    return render(request, 'internal/request/index.html', {'requests' : Request.objects.all()})


def create(request):
    context = {}

    return render(request, 'internal/request/create.html', context)


def store(request):
    context = {'message': 'Solicitud creada exitosamente'}

    return redirect('internal:request.index')
