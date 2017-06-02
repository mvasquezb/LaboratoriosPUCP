from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/testType/index.html',
          extra_context=None):
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)

def create(request,
          template='internal/testType/create.html',
          extra_context=None):
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)

def edit(request,
          template='internal/testType/edit.html',
          extra_context=None):
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)
