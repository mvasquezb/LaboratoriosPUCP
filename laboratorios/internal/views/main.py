from django.shortcuts import render
from django.http import HttpResponse
from ..models import Product


#__all__ = (
#    'index',
#)


def index(request,
          template='internal/index.html',
          extra_context=None):
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
