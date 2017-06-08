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
    search = request.GET.get('search')
    if search:
        laboratory_list = Laboratory.objects.filter(
            name__icontains=search).order_by ('name')
    else:
        laboratory_list = Laboratory.objects.order_by ('name')

    paginator = Paginator(laboratory_list, 3)
    page = request.GET.get('page')
    try:
        laboratorys = paginator.page (page)
    except PageNotAnInteger:
        laboratorys = paginator.page(1)
    except EmptyPage:
        laboratorys = paginator.page(paginator.num_pages)

    context = {
        'laboratorys_list': laboratorys,
        'paginator': paginator,
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
