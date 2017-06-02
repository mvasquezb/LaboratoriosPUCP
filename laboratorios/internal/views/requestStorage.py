from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *

def index(request,
          template='internal/requestStorage/index.html',
          extra_context=None):
    types = RequestStorage.objects.all()
    context = {'requestStorage_list': types}
    return render(request, template, context)

def aprobar(request,
          template='internal/requestStorage/index.html',
          extra_context=None):
    print(request.GET)
    if request.method == 'GET' and 'array[]' in request.GET:
        #print("flag2")
        x = dict(request.GET)
        for i in x['array[]']:
            old = RequestStorage.objects.get(pk=i)
            old.pendiente = False
            old.aprobado = True
            old.save()
    print("flag3")
    types = RequestStorage.objects.all()
    context = {'requestStorage_list': types}
    return render(request, template, context)
    #return redirect('requestStorage.index')

def rechazar(request,
          template='internal/requestStorage/index.html',
          extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            old = RequestStorage.objects.get(pk=i)
            old.pendiente = False
            old.aprobado = False
            old.save()

    types = RequestStorage.objects.all()
    context = {'requestStorage_list': types}
    return render(request, template, context)
