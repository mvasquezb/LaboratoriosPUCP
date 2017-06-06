from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *

def index(request,
          template='internal/laboratory/index.html',
          extra_content=None):
    context = {}
    return render(request, template, context)

def create(request,
          template='internal/laboratory/create.html',
          extra_content=None):
    users = Employee.objects.all()
    context = {'users': users}
    return render(request, template, context)