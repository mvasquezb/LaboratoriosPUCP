from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from .forms import LaboratoryForm
from internal.models import *

def index(request,
          template='internal/laboratory/index.html',
          extra_content=None):
    labs = Laboratory.objects.all()
    context = {'labs': labs}
    return render(request, template, context)

def create(request,
          template='internal/laboratory/create.html',
          extra_content=None):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('internal:laboratory.index')
        else:
            return HttpResponse(str(form.errors))
    else:
        users = Employee.objects.all()
        service_hours = LaboratoryServiceHours.objects.all()
        inventories = Inventory.objects.all()
        essaymethods = EssayMethod.objects.all()
        form = LaboratoryForm()
        context = {'users': users, 'service_hours': service_hours, 'inventories': inventories,
                   'essaymethods': essaymethods, 'form': form}
        return render(request, template, context)

def edit(request,
        pk):
    if request.method == 'POST':
        print("snd")
    else :
        laboratory = Laboratory.objects.get(pk=pk)
        users = Employee.objects.all()
        service_hours = LaboratoryServiceHours.objects.all()
        inventories = Inventory.objects.all()
        essaymethods = EssayMethod.objects.all()
        form = LaboratoryForm()
        context = {'users': users, 'service_hours': service_hours, 'inventories': inventories,
                   'essaymethods': essaymethods, 'form': form, 'laboratory': laboratory}
        template = 'internal/laboratory/edit.html'
        return render(request, template, context)