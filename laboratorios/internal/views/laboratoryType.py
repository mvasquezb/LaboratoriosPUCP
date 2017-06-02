from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/laboratoryType/index.html',
          extra_context=None):
    labtypes = LaboratoryType.objects.all()
    essaytypes= EssayType.objects.all()
    sampletypes=SampleType.objects.all()
    context = {'labType_list': labtypes,'essayType_list':essaytypes,'sampleType_list':sampletypes}
    return render(request, template, context)


def validation_name(name):
    all_elements = LaboratoryType.objects.all()
    for i in all_elements:
        if name==i.name:
            return False
    return True


def create(request,
           template='internal/laboratoryType/create.html',
           extra_context=None):
    essaytypes = EssayType.objects.all ()
    sampletypes = SampleType.objects.all ()
    if request.method == 'POST':
        index='internal/laboratoryType/index.html'
        labtypes = LaboratoryType.objects.all ()
        context = {'laboratoryType_list':labtypes}
        if "b_cancel" in request.POST:
            return redirect('internal:laboratoryType.index')
        if "b_submit" in request.POST:
            name = str(request.POST.get ('textname'))
            description = str(request.POST.get ('description'))
            if validation_name(name):
                lab_type = LaboratoryType.objects.create (
                    name=name,
                    description=description,
                    active=True
                )
    context = {'essayType_list': essaytypes, 'sampleType_list': sampletypes}
    return render(request, template, context)


def create2(request):
    essaytypes = EssayType.objects.all ()
    sampletypes = SampleType.objects.all ()
    template = 'internal/laboratoryType/create.html'
    if request.method == 'GET':
        x = dict(request.GET)
        lab_type = LaboratoryType.objects.get(name="Corrosion") # El nombre que reciba como parametro
        for i in x['array[]']:
            sample= SampleType.objects.get(name=i)
            if sample:
                sample.lab_type = lab_type
                sample.save ()
        essaytypes = EssayType.objects.all()
        sampletypes = SampleType.objects.all()
        context = {'essayType_list': essaytypes, 'sampleType_list': sampletypes}
        return render(request, template, context)
    context = {'essayType_list': essaytypes, 'sampleType_list': sampletypes}
    return render(request, template, context)

def edit(request,
           template='internal/laboratoryType/edit.html',
           extra_context=None):
    essaytypes = EssayType.objects.all()
    sampletypes = SampleType.objects.all()
    context = {'essayType_list': essaytypes, 'sampleType_list': sampletypes}
    return render(request, template, context)


def delete(request,
          template='internal/laboratoryType/index.html',
          extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            LaboratoryType.objects.filter(pk=i).delete()
    labtypes = LaboratoryType.objects.all()
    essaytypes = EssayType.objects.all()
    sampletypes = SampleType.objects.all()
    context = {'labType_list': labtypes, 'essayType_list': essaytypes, 'sampleType_list': sampletypes}
    return render (request, template, context)
