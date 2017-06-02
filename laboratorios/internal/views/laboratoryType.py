from django.shortcuts import render,redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *
import time

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
    if request.method == 'GET'and request.is_ajax():
        x = dict(request.GET)
        lab_type = LaboratoryType.objects.create(
            name=x['name'][0],
            description="",
            active=True
        )
        for i in x['array[]']:
            cutName = i[1:]
            print(cutName)
            if i[0]=='S':
                sample = SampleType.objects.get(name=cutName)
                if sample:
                    sample.lab_type = lab_type
                    sample.save()
            else:
                essay = EssayType.objects.get(name=cutName)
                if essay:
                    essay.lab_type = lab_type
                    essay.save()
        return redirect('internal:laboratoryType.create')
    if request.method == 'POST':
        index='internal/laboratoryType/index.html'
        labtypes = LaboratoryType.objects.all ()
        context = {'laboratoryType_list':labtypes}
        if "b_cancel" in request.POST:
            return render(request, index, context)
        if "b_submit" in request.POST:
            time.sleep(1)
            name = str(request.POST.get ('textname'))
            description = str(request.POST.get ('description'))
            lab_type = LaboratoryType.objects.get(name=name)
            lab_type.description = description


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
