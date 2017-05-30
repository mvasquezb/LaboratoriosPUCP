from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/sampleType/index.html',
          extra_context=None):
    labtypes = LaboratoryType.objects.all()
    sampletypes=SampleType.objects.all()
    context = {'labType_list': labtypes,'sampleType_list':sampletypes}
    return render(request, template, context)


def create(request,
           template='internal/sampleType/create.html',
           extra_context=None):
    labtypes = LaboratoryType.objects.all ()
    sampletypes = SampleType.objects.all ()
    context = {'labType_list': labtypes, 'sampleType_list': sampletypes}
    return render(request, template, context)


def edit(request,
           template='internal/sampleType/edit.html',
           extra_context=None):
    labtypes = LaboratoryType.objects.all ()
    sampletypes = SampleType.objects.all ()
    context = {'labType_list': labtypes, 'sampleType_list': sampletypes}
    return render(request, template, context)
