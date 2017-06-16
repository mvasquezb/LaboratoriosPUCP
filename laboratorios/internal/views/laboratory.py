from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from internal.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .forms import LaboratoryForm


def index(request,
          template='internal/laboratory/index.html',
          extra_context=None):
    laboratorys = Laboratory.all_objects.all()
    context = {
        'laboratorys_list': laboratorys
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def create(request,
          template='internal/laboratory/create.html',
          extra_content=None):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha creado un nuevo laboratorio exitosamante!')
            return redirect('internal:laboratory.index')
        else:
            messages.error(request, 'Ya existe un laboratorio con el mismo nombre, ingrese otro')
            #return HttpResponse(status=204)
            return redirect('internal:laboratory.create')
    else:
        users = Employee.all_objects.filter(deleted__isnull=True)
        service_hours = LaboratoryServiceHours.all_objects.filter(deleted__isnull=True)
        inventories = Inventory.all_objects.filter(deleted__isnull=True)
        essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        form = LaboratoryForm()
        context = {'users': users, 'service_hours': service_hours, 'inventories': inventories,
                   'essaymethods': essaymethods, 'form': form}
        return render(request, template, context)

def edit(request,
        pk):
    if request.method == 'POST':
        instance = Laboratory.objects.get(pk=pk)
        aux_form = LaboratoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            aux_form.save()
            messages.success(request, 'Se ha editado el laboratorio exitosamante')
            return redirect('internal:laboratory.index')
        else:
            messages.error(request, 'Ya existe un laboratorio con el mismo nombre, ingrese otro')
            #return HttpResponse(status=204)
            return redirect('internal:laboratory.edit', pk=pk)
    else :
        laboratory = Laboratory.objects.get(pk=pk)
        #
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = laboratory.employees.all()
        #
        all_service_hours = LaboratoryServiceHours.all_objects.filter(deleted__isnull=True)
        selected_service_hours = laboratory.service_hours
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {'laboratory': laboratory, 'all_users': all_users,
                   'selected_users': selected_users, 'all_service_hours': all_service_hours,
                   'selected_service_hours': selected_service_hours,
                   'all_inventories': all_inventories, 'selected_inventories': selected_inventories,
                   'all_essaymethods': all_essaymethods, 'selected_essaymethods': selected_essaymethods,
                   'form': form}
        template = 'internal/laboratory/edit.html'
        return render(request, template, context)


def delete(request, pk):
    laboratory = get_object_or_404(Laboratory, pk=pk)
    laboratory.delete()
    messages.success(request, 'Se ha borrado el laboratorio existosamente')
    return redirect('internal:laboratory.index')

def show(request,
        pk):
    if request.method == 'POST':
        instance = Laboratory.objects.get(pk=pk)
        aux_form = LaboratoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            aux_form.save()
            return redirect('internal:laboratory.index')
    else :
        laboratory = Laboratory.objects.get(pk=pk)
        #
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = laboratory.employees.all()
        #
        all_service_hours = LaboratoryServiceHours.all_objects.filter(deleted__isnull=True)
        selected_service_hours = laboratory.service_hours
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {'laboratory': laboratory, 'all_users': all_users,
                   'selected_users': selected_users, 'all_service_hours': all_service_hours,
                   'selected_service_hours': selected_service_hours,
                   'all_inventories': all_inventories, 'selected_inventories': selected_inventories,
                   'all_essaymethods': all_essaymethods, 'selected_essaymethods': selected_essaymethods,
                   'form': form}
        template = 'internal/laboratory/show.html'
        return render(request, template, context)
