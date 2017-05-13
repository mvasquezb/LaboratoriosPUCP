from django.shortcuts import render
from django.http import HttpResponse
from internal.models import Product, Sale


def index(request, template='internal/index.html', extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def lista_productos(request,
          template='internal/lista_productos.html',
          extra_context=None):
    productos= Product.objects.all()
    context = {'productos':productos}
    if extra_context is not None:
        context.update (extra_context)
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
