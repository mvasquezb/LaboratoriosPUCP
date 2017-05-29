from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from internal.models import TestTemplate


def index(request):
    return render(request, 'internal/test/index.html', {'tests': TestTemplate.objects.all()})


def create(request):
    context = {}

    return render(request, 'internal/test/create.html', context)


def store(request):
    context = {'message': 'Prueba creada exitosamente'}

    return redirect('internal:test.index')
