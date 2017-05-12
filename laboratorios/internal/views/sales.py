from django.shortcuts import render
from django.http import HttpResponse
from internal import models


def index(request):
    return HttpResponse("Lista de ventas")


def create(request):
    if request.method == 'POST':
        s_amount = request.POST.get('s_amount')
        if s_amount:
            sale = models.Sale(ammount=s_amount)
            sale.save()
    context = {}
    template = 'internal/sales_create.html'
    return render(request, template, context)
