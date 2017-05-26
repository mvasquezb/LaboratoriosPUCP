from django.shortcuts import render

from django.http import HttpResponse, HttpResponseRedirect
from ..models import *

def index(request,
          template='internal/Labs/createLabs.html',
          extra_context=None):
    typelabs = TypeLabs.objects.all()
    context ={'types': typelabs}
    return render(request, template, context)

def create(request):

    if request.method == 'POST':
        name = str(request.POST.get('textname'))
        numberUsers = int(request.POST.get('numberUsers'))
        capacity2 = int(request.POST.get('text_capacity'))
        typeLabs = str(request.POST.get('comboBox_type'))
        TypeLabObject = TypeLabs.objects.get(typename = typeLabs)
        if name:
            lab = Labs.objects.create(labname=name,numUser=numberUsers,capacity=capacity2,active=True,typeLab=TypeLabObject)
    return HttpResponse("Laboratoio de " + name + str(numberUsers) + str(capacity2) + "tipo: " + str(typeLabs) + "Creado exitosamente")

def list(request,
         template='internal/Labs/listLabs.html',
          extra_context=None):
    labs = Labs.objects.all()
    context ={'lista_labs': labs}
    return render(request, template, context)
