from django.shortcuts import render
from django.shortcuts import render_to_response
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
    product = models.Product.objects.get(id=id)
    if product:
        product.description = request.POST['description']
        product.unit_cost= request.POST['unit_cost']
        product.save()
        return render(request, 'internal/index.html')
