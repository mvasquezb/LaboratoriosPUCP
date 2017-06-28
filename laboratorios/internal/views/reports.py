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
    #squared = list(map(lambda x: x**2, items))
    data_list={
        'client': list(map((lambda x: {'id':x.id,'str':x.user}),Client.all_objects.filter(deleted__isnull=True).order_by('user','id')[::1])),
        'sample_type': list(map(lambda x: {'id':x.id,'str':x.name},SampleType.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1])),
        'laboratory':list(map(lambda x: {'id':x.id,'str':x.name},Laboratory.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1])),
        'essay':list(map(lambda x: {'id':x.id,'str':x.name},Essay.all_objects.filter(deleted__isnull=True).order_by('name','id')[::1]))
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

    criteria_selection=[
        'client',
        'sample_type',
        'laboratory',
        'essay',
    ]
    criteria_selection_string = ['Cliente','Tipo de Muestra','Laboratorio','Ensayo']

    # The JSONField wil pickup the following:
    # 1.- Date Range
    # 2.- Dictionary of selected filter
    # 3.- Expected type of report and chart -- to be seen lmao
    # 4.- filter selection structure, as context itself is immutable
    json_form = JSONField(request.POST or None)

    context = {
        'filter':filter_selection,
        'filter_string':filter_selection_string,
        'data_list':data_list,
        'criteria_string':criteria_selection_string,
        'json_form': json_form,
        }
    if request.method == 'POST':
        print('hello?')
        js_data = json.loads(json_form['js_data'].value())
        if js_data is not None:
            js_data.update({
                            'filter':filter_selection,
                            'criteria_list':criteria_selection,
                            'data_list':dict(map(lambda x: (x[0],list(map(lambda y: y['id'], x[1] ))) , data_list.items())),
                            'start_date':js_data['start_date'][:10],
                            'end_date':js_data['end_date'][:10],
                            })
            request.session['report_settings']=js_data
            request.session.modified = True
            return redirect(reverse('internal:reports.results'))
        else:
            print("que fuentes tmr?")
    return render(request,template,context)

def client_group(context,settings):
    # Filas        
    # Num servicios en rango de fechas
    table_label=['Nombre de Cliente', 'Número de Servicios','Costo promedio por Servicio','Costo acumulado de Servicios','Duración promedio de servicios']
    table_matrix=[]
    # Etapa de filtracion de resultados
    if (len(settings['filters_data'][0]) >0):
        client_list=list(map(lambda x:Client.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['client'][x],settings['filters_data'][0]))))
    else:
        client_list=Client.all_objects.filter(deleted__isnull=True)[::1]
    service_matrix=list(map(lambda x:ServiceRequest.all_objects.filter(deleted__isnull=True,client=x)[::1],client_list))

    if(len(settings['filters_data'][1]) >0):
        sample_list=list(map(lambda x:SampleType.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['sample_type'][x],settings['filters_data'][1]))))
        service_matrix=list(map(lambda x: [y for y in x if len(Sample.all_objects.filter(deleted__isnull=True,request=y,sample_type__in=sample_list))>0],service_matrix))

    if(len(settings['filters_data'][2])>0):
        laboratory_list=list(map(lambda x:Laboratory.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['laboratory'][x],settings['filters_data'][2]))))
        service_matrix=list(map(lambda x: [y for y in x if y.supervisor.laboratories.all().first() in laboratory_list],service_matrix))
    if(len(settings['filters_data'][3])>0):
        essay_list=list(map(lambda x:Essay.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['essay'][x],settings['filters_data'][3]))))
        service_matrix=list(map(lambda x: [y for y in x if len(EssayFill.all_objects.filter(deleted__isnull=True,essay__in=essay_list,sample=y.sample))>0],service_matrix))

   ## print(client_list)  
   ## print(sample_list)
   ## print(laboratory_list)
   ##s print(service_matrix)
    return context

def sample_group(context,settings):
    return context

def laboratory_group(context,settings):
    # Filas         Num Empleados, Num Servicios dentro de fechas, Num 
    return context

def essay_group(context,settings):
    return context

def processing_parameters(
    request,
    template='internal/reports/results.html'
    ):
    try:
        settings=request.session.get('report_settings',[])
        print(settings)
    except KeyError:
        print('not there yet')
        settings={}
    context={}
    if (len(settings) == 0):
        return render(request,template,context)
    # we only recieve id as those are what we need to reconstruct our list
    if len(settings['criteria_list'])==settings['criteria']:
        return render(request,template,context)
    mycase = {
        'client': client_group, #do not use ()
        'sample_type': sample_group, #do not use ()
        'laboratory': laboratory_group, #do not use ()
        'essay': essay_group,
    }

    return render(request,template,mycase[settings['criteria_list'][settings['criteria']]](context,settings))

    