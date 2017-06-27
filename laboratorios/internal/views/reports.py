from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from django.db.models import (
    Sum,
    Q,
    When,
    Case,
    Value,
    F,
)
from django.urls import *
import json
from datetime import *
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib import messages

from internal.models import *
from internal.views.forms import *
from django.core import serializers

def report_parameters(request,
    template='internal/reports/start.html'):
    # so clearly, context would carry most of the data, so then its a JSON
    # First filter is range of dates, which doesnt need any from db
    # Second filter is client, which we do have
    
    # as we do not want to mantain later the logic bc of more fitlers,
    # lets use a dictionary
    data_list={
        'client':[o.__str__() for o in Client.all_objects.filter(deleted__isnull=True).order_by('user','id')[::1]],
        'sample_type':[o.name for o in SampleType.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1]],
        'laboratory':[o.name for o in Laboratory.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1]],
        'essay':[o.name for o in Essay.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1]]
    }

    # Because we wont always check for all filters, we should have a
    # register which expose so

    filter_selection = [
        'client',
        'sample_type',
        'laboratory',
        'essay'
        ]

    filter_selection_string={
        'client':'Cliente',
        'sample_type':'Tipo de Muestra',
        'laboratory':'Laboratorio',
        'essay':'Ensayo',
    }

    criteria_selection_string = ['Cliente','Tipo de Muestra','Laboratorio','Ensayo']

    # The JSONField wil pickup the following:
    # 1.- Date Range
    # 2.- Dictionary of selected filter
    # 3.- Expected type of report and chart -- to be seen lmao
    # 4.- filter selection structure, as context itself is immutable

    context = {
        'filter':filter_selection,
        'filter_string':filter_selection_string,
        'data_list':data_list,
        'criteria_string':criteria_selection_string,
        }
    if request.method == 'POST':
        ## processing of shit right here
        print('hola?')
        print(request.body)
        js_data = json.loads(request.body.decode('utf-8'))['js_data']
        if js_data is not None:
            print(js_data)
            return redirect(reverse('internal:reports.results',kwargs={'settings_string': js_data}))
        else:
            print("que fuentes tmr?")
    return render(request,template,context)



def processing_parameters(
    request,
    settings_string,
    template='internal/reports/results.html'
    ):
    print(settings_string)
    context={}

    return render(request,template,context)