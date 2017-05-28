from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/assayType/index.html',
          extra_context=None):
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)
