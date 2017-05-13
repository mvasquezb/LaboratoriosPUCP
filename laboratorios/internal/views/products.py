from django.shortcuts import render, get_object_or_404
from django.template import RequestContext

from django.http import HttpResponse
from internal import models


def index(request):
    return HttpResponse("Lista de Productos")


def edit(request, id):
    product = models.Product.objects.get(id=id)

    return render(request, 'internal/products/form.html',
         { 'action': 'update/' + id,
         'button': 'Actualizar',
         'description': product.description,
         'unit_cost': product.unit_cost
         }
     )


def update(request, id):
    product = get_object_or_404(models.Product, id=id)
    if product:
        product.description = request.POST.get('description')
        product.unit_cost = request.POST.get('unit_cost')
        product.save()
    return render(request, 'internal/index.html')


def create(request):
    if request.method == 'POST':
        descri = request.POST.get('fdescrip')
        costo = float(request.POST.get('fcosto'))
        if costo and descri:
            product = models.Product.objects.create(description=descri, unit_cost=costo)

    context = {}
    template = 'internal/products/create.html'
    return render(request, template, context)
