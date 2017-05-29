from django.shortcuts import render
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


def create(request,
           template='internal/laboratoryType/create.html',
           extra_context=None):
    essaytypes = EssayType.objects.all ()
    sampletypes = SampleType.objects.all ()
    context = {'essayType_list': essaytypes, 'sampleType_list': sampletypes}
    return render(request, template, context)
