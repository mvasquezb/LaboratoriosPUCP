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
from .forms import SampleTypeForm

NOT_OPTION_SELECTED="Selecciona una opcion"

def index(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    search = request.GET.get ('search')
    if search:
        sampleType_list = SampleType.objects.filter (
            name__icontains=search).order_by ('name')
    else:
        sampleType_list = SampleType.objects.order_by ('name')

    paginator = Paginator (sampleType_list, 3)
    page = request.GET.get ('page')
    try:
        sampletypes = paginator.page (page)
    except PageNotAnInteger:
        sampletypes = paginator.page (1)
    except EmptyPage:
        laboratorys = paginator.page (paginator.num_pages)

    context = {
        'sampleType_list': sampletypes,
        'paginator': paginator,
    }
    if extra_context is not None:
        context.update (extra_context)
    return render (request, template, context)

def validation_name(name):
    all_elements = SampleType.objects.all()
    for i in all_elements:
        if name==i.name:
            return False
    return True

def create(request,
           template='internal/SampleType/create.html',
           extra_context=None):
    sampletypes = SampleType.objects.all ()
    context = {'sampleType_list':sampletypes}
    if request.method == 'POST':
        index='internal/SampleType/index.html'
        if "b_cancel" in request.POST:
            return redirect('internal:SampleType.index')
        if "b_submit" in request.POST:
            name = str (request.POST.get ('textname'))
            description = str(request.POST.get ('description'))
            lab_type_choose = str (request.POST.get('labType_combobox'))
            if validation_name (name):
                if(lab_type_choose!=NOT_OPTION_SELECTED):
                    sample_type = SampleType.objects.create (
                        name=name,
                        description=description,
                        active=True,
                        lab_type=lab_type
                    )
                else:
                    sample_type = SampleType.objects.create (
                        name=name,
                        description=description,
                        active=True
                    )
            return redirect('internal:SampleType.index')
    return render(request, template, context)


def edit(request,id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect ('internal:SampleType.index')
        if "b_submit" in request.POST:
            oldsampletype = SampleType.objects.get(pk=id)
            name = str (request.POST.get ('textname'))
            description = str (request.POST.get ('description'))
            lab_type_choose = str (request.POST.get ('labType_combobox'))
            if validation_name (name):
                oldsampletype.name=name
                oldsampletype.description=description
                oldsampletype.active=True
                if (lab_type_choose != NOT_OPTION_SELECTED):
                    lab_type = LaboratoryType.objects.get (name=lab_type_choose)
                    oldsampletype.lab_type=lab_type
                else:
                    oldsampletype.lab_type=None
                oldsampletype.save()
            return redirect('internal:SampleType.index')
    else:
        sample = SampleType.objects.get(pk=id)
        sampletypes = SampleType.objects.all()
        context = {'sample': sample, 'sampleType_list': sampletypes}
        template = 'internal/SampleType/edit.html'
        return render (request, template, context)


def delete(request,
          template='internal/SampleType/index.html',
          extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            SampleType.objects.filter(pk=i).delete()
    sampletypes = SampleType.objects.all ()
    context = { 'sampleType_list': sampletypes}
    return render(request, template, context)
