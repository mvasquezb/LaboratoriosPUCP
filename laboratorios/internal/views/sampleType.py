from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect

from ..models import *

NOT_OPTION_SELECTED="Selecciona una opcion"

def index(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    labtypes = LaboratoryType.objects.all()
    sampletypes=SampleType.objects.all()
    context = {'labType_list': labtypes,'sampleType_list':sampletypes}
    return render(request, template, context)

def validation_name(name):
    all_elements = SampleType.objects.all()
    for i in all_elements:
        if name==i.name:
            return False
    return True

def create(request,
           template='internal/sampleType/create.html',
           extra_context=None):
    labtypes = LaboratoryType.objects.all()
    sampletypes = SampleType.objects.all ()
    context = {'labType_list': labtypes,'sampleType_list':sampletypes}
    if request.method == 'POST':
        index='internal/sampleType/index.html'
        if "b_cancel" in request.POST:
            return redirect('internal:sampleType.index')
        if "b_submit" in request.POST:
            labtypes = LaboratoryType.objects.all ()
            name = str (request.POST.get ('textname'))
            description = str(request.POST.get ('description'))
            lab_type_choose = str (request.POST.get('labType_combobox'))
            if validation_name (name):
                if(lab_type_choose!=NOT_OPTION_SELECTED):
                    lab_type = LaboratoryType.objects.get(name=lab_type_choose)
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
            return redirect('internal:sampleType.index')
    return render(request, template, context)


def edit(request,id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect ('internal:sampleType.index')
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
            return redirect('internal:sampleType.index')
    else:
        sample = SampleType.objects.get(pk=id)
        labtypes = LaboratoryType.objects.all()
        sampletypes = SampleType.objects.all()
        context = {'sample': sample,'labType_list': labtypes, 'sampleType_list': sampletypes}
        template = 'internal/sampleType/edit.html'
        return render (request, template, context)


def delete(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            SampleType.objects.filter(pk=i).delete()
    labtypes = LaboratoryType.objects.all ()
    sampletypes = SampleType.objects.all ()
    context = {'labType_list': labtypes, 'sampleType_list': sampletypes}
    return render(request, template, context)
