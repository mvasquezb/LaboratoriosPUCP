from django.http import HttpResponse
from django.shortcuts import render

from ..models import Sale
__all__ = (
    'index',
)


def index(request,
          template='internal/index.html',
          extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def editar_ventas(request,
          template='internal/editar_ventas.html',
          extra_context=None):
    venta_shida = Sale.objects.get(id = 1)
    if(venta_shida):
        venta_shida.ammount = 3.1416;
        venta_shida.save()
    context = {'venta_shida': venta_shida}
    return render(request, template, context)


def lista_ventas(request,
          template='internal/lista_ventas.html',
          extra_context=None):
    ventas = Sale.objects.all()
    context ={'ventas': ventas}
    #context = {}
    # if extra_context is not None:
    #    context.update(extra_context)
    return render(request, template, context)

#Suma simple
#Hecho por Chic Cherry Cola <3
def sumita(request,
           number_1,
           number_2):

    return HttpResponse("La suma de %s y %s es: %d" % (number_1, number_2, int(number_1) + int(number_2)) )
