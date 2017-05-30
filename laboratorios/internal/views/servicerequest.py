from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from internal.models import ServiceRequest


def index(request):
    return render(request, 'internal/servicerequest/index.html', {'requests': ServiceRequest.objects.all()})


def create(request):
    context = {}
    return render(request, 'internal/servicerequest/create.html', context)


def store(request):
    context = {'message': 'Solicitud creada exitosamente'}
    return redirect('internal:servicerequest.index')
