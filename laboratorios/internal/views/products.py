from django.shortcuts import render
from django.http import HttpResponse
from internal import models


def index(request):
    return HttpResponse("Lista de productos")


def create(request):
    if request.method == 'POST':
        descri = request.POST.get('fdescrip')
        costo = float(request.POST.get('fcosto'))
        if costo and descri:
            product = models.Product.objects.create(description=descri, unit_cost=costo)

    context = {}
    template = 'internal/products/create.html'
    return render(request, template, context)
