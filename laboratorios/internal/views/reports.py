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
from pprint import pprint
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
import time
import datetime
from datetime import date
from functools import reduce

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

def quotation_price(essay_list):
    essay_list = essay_list.annotate(
        price=Sum(
            Case(
                When(
                    essaymethodfill__chosen=True,
                    then=F('essaymethodfill__essay_method__price')
                ),
                default=Value(0)
            )
        )
    )

    total_price = sum([
        essay.price
        if essay.price else 0
        for essay in essay_list
    ])
    return total_price

def client_group(request,context,settings):
    # Filas        
    # Num servicios en rango de fechas
    table_label=['Nombre de Cliente', 'Número de Servicios','Promedio de Muestras por Servicio','Costo acumulado de Servicios','Costo promedio por Servicio','Duración promedio de servicios']
    table_matrix=[]
    # Results filtering 

    # client filtering
    if (len(settings['filters_data'][0]) >0):
        client_list=list(map(lambda x:Client.all_objects.filter(deleted__isnull=True,pk=x).first(), list(map(lambda x: settings['data_list']['client'][x],settings['filters_data'][0]))))
    else:
        client_list=Client.all_objects.filter(deleted__isnull=True)[::1]
    print(client_list)
    # end client filtering

    # date filtering
    start_date=datetime.date(int(settings['start_date'][0:4]),int(settings['start_date'][5:7]),int(settings['start_date'][8:10]))
    end_date=datetime.date(int(settings['end_date'][0:4]),int(settings['end_date'][5:7]),int(settings['end_date'][8:10]))
    service_matrix=list(map(lambda x: ServiceRequest.all_objects.filter(deleted__isnull=True,client=x)[::1],client_list))
    print(service_matrix)
    service_matrix=list(map(lambda x: [y for y in x if start_date<=y.registered_date.date()<=end_date],service_matrix))
    print(service_matrix)
    # end date filtering

    # sample filtering
    if(len(settings['filters_data'][1]) >0):
        sample_list=list(map(lambda x:SampleType.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['sample_type'][x],settings['filters_data'][1]))))
        print(sample_list)
        service_matrix=list(map(lambda x: [y for y in x if len(Sample.all_objects.filter(deleted__isnull=True,request=y,sample_type__in=sample_list))>0],service_matrix))
    print(service_matrix)
    #end sample filtering

    # laboratory filtering
    if(len(settings['filters_data'][2])>0):
        laboratory_list=list(map(lambda x:Laboratory.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['laboratory'][x],settings['filters_data'][2]))))
        print(laboratory_list)
        service_matrix=list(map(lambda x: [y for y in x if y.supervisor.laboratory in laboratory_list],service_matrix))
    print(service_matrix)
    #end laboratory filtering

    # essay filtering
    if(len(settings['filters_data'][3])>0):
        essay_list=list(map(lambda x:Essay.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['essay'][x],settings['filters_data'][3]))))
        service_matrix=list(map(lambda x: [y for y in x if len(EssayFill.all_objects.filter(deleted__isnull=True,essay__in=essay_list,sample=y.sample))>0],service_matrix))
    print(service_matrix)
    # end essay filtering    

    # data processing
    results =[]
    for i in range(0,len(client_list)):
        aux_list=[]
        aux_list.append(client_list[i])
        aux_list.append(len(service_matrix[i]))
        print(i)
        try:
            aux_list.append(sum([len(x) for x in [Sample.all_objects.filter(deleted__isnull=True,request=z) for z in service_matrix[i]]])/aux_list[1])
        except:
            aux_list.append(0)
        try:
            aux_list.append(sum([x[0] for x in list(map(lambda z: [quotation_price(EssayFill.all_objects.filter(deleted__isnull=True,sample=y)) for y in Sample.all_objects.filter(deleted__isnull=True,request=z)] ,service_matrix[i])) if len(x)>0]))
        except:
            aux_list.append(0)
        if aux_list[1]>0 and aux_list[3]:
            print(aux_list[3])
            aux_list.append(aux_list[3]/aux_list[1])
            aux_list.append(sum([x.expected_duration for x in service_matrix[i]])/aux_list[1])
        else:
            aux_list.append(0)
            aux_list.append(0)
        results.append(aux_list)
    print(results)
    modal_matrix = list(map(lambda x :[[y.client.user.first_name+' '+y.client.user.last_name,  y.supervisor.user.first_name+' '+y.supervisor.user.last_name, y.state.description ,y.observations] for y in x], service_matrix))
    request.session['modal_matrix'] = modal_matrix
    request.session['modal_labels'] = ['Cliente','Supervisor','Estado','Observaciones']

    context={
        'group_type':'Cliente',
        'start_date':start_date,
        'end_date':end_date,
        'data_labels':table_label,
        'results':results,
        'modal_index' : -1,
        'modal_matrix' : modal_matrix
        }


    # end data processing
    return context


def sample_group(request, context,settings):
    # Columnas
    table_label=['Tipo de muestra', 'Número de Muestras','Promedio de Métodos por Muestra','Costo acumulado de Métodos','Costo promedio por Método']
    table_matrix=[]

    # sample type filtering
    if (len(settings['filters_data'][1])>0):
        sample_list=list(map(lambda x:SampleType.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['sample_type'][x],settings['filters_data'][1]))))
    else:
        sample_list=SampleType.all_objects.filter(deleted__isnull=True)[::1]
    # end sample type filtering

    # date filtering
    start_date=datetime.date(int(settings['start_date'][0:4]),int(settings['start_date'][5:7]),int(settings['start_date'][8:10]))
    end_date=datetime.date(int(settings['end_date'][0:4]),int(settings['end_date'][5:7]),int(settings['end_date'][8:10]))
    sample_matrix=list(map(lambda x: Sample.all_objects.filter(deleted__isnull=True,sample_type=x),sample_list))
    sample_matrix=list(map(lambda x: [y for y in x if start_date<=y.registered_date.date()<=end_date],sample_matrix))
    print(sample_matrix)
    # end date filtering


    # client filtering
    if (len(settings['filters_data'][0])>0):
        client_list=list(map(lambda x:Client.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['client'][x],settings['filters_data'][0]))))
        print(client_list)
        sample_matrix=list(map(lambda x:[y for y in x if y.request.client in client_list],sample_matrix))
    print(sample_matrix)
    # end client filtering

    # laboratory filtering
    if (len(settings['filters_data'][2])>0):
        laboratory_list=list(map(lambda x:Laboratory.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['laboratory'][x],settings['filters_data'][2]))))
        print(laboratory_list)
        sample_matrix=list(map(lambda x:[y for y in x if y.request.supervisor.laboratory in laboratory_list],sample_matrix))
    print(sample_matrix)
    # end laboratory filtering

    # essay filtering
    if (len(settings['filters_data'][3])>0):
        essay_list=list(map(lambda x:Essay.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['essay'][x],settings['filters_data'][3]))))
        print(essay_list)
        sample_matrix=list(map(lambda x:[y for y in x if EssayFill.all_objects.filter(deleted__isnull=True,sample=y,essay__in=essay_list) ],sample_matrix))
    print(sample_matrix)
    # end essay filtering
    
    # data processing
    results=[]
    for i in range(0,len(sample_list)):
        aux_list=[]
        aux_list.append(sample_list[i])
        aux_list.append(len(sample_matrix[i]))
        aux_method_list=[val for sublist in [EssayMethodFill.all_objects.filter(deleted__isnull=True,essay=EssayFill.all_objects.filter(deleted__isnull=True,sample=z).first(),chosen=True)[::1] for z in sample_matrix[i]] for val in sublist]
        try:
            aux_list.append(len(aux_method_list)/aux_list[1])
        except:
            aux_list.append(0)
        try:
            aux_list.append(sum([x.essay_method.price for x in aux_method_list]))
        except:
            aux_list.append(0)
        try:
            aux_list.append(aux_list[3]/aux_list[1])
        except:
            aux_list.append(0)
        results.append(aux_list)

    modal_matrix = list(map(lambda x :[[y.code,  y.name,y.description, y.registered_date.strftime("%Y-%m-%d %H:%M:%S")] for y in x], sample_matrix))
    request.session['modal_matrix'] = modal_matrix
    request.session['modal_labels']=['Código','Nombre','Descripción','Fecha de registro']

    context={
        'group_type':'Tipo de Muestra',
        'start_date':start_date,
        'end_date':end_date,
        'data_labels':table_label,
        'results':results,
        'modal_index' : -1,
        'modal_matrix' : modal_matrix
        }

    return context

def laboratory_group(request,context,settings):
    # Filas         Num Empleados, Num Servicios dentro de fechas, Num 
    # Columnas
    table_label=['Laboratorio', 'Número de Servicios','Promedio de Muestras por Servicio','Costo acumulado de Servicios','Costo promedio por Servicio','Duración promedio de servicios']
    table_matrix=[]

    # Filtro por Laboratorio
    if (len(settings['filters_data'][2])>0):
        laboratory_list=list(map(lambda x:Laboratory.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['laboratory'][x],settings['filters_data'][2]))))
    else:
        laboratory_list=Laboratory.all_objects.filter(deleted__isnull=True)[::1]
    print(laboratory_list)

    # Filtro por Fechas
    start_date=datetime.date(int(settings['start_date'][0:4]),int(settings['start_date'][5:7]),int(settings['start_date'][8:10]))
    end_date=datetime.date(int(settings['end_date'][0:4]),int(settings['end_date'][5:7]),int(settings['end_date'][8:10]))
    service_matrix=[[x for x in ServiceRequest.all_objects.filter(deleted__isnull=True) if x.supervisor.laboratory == y] for y in laboratory_list]    
    print(service_matrix)
    service_matrix=list(map(lambda x: [y for y in x if start_date<=y.registered_date.date()<=end_date],service_matrix))
    print(service_matrix)
    # Fin filtro por Fechas

    # Filtro por cliente
    # client filtering
    if (len(settings['filters_data'][0])>0):
        client_list=list(map(lambda x:Client.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['client'][x],settings['filters_data'][0]))))
        print(client_list)
        service_matrix=list(map(lambda x:[y for y in x if y.client in client_list],service_matrix))
    print(service_matrix)
    # End client filtering

    # Sample Type filtering
    if(len(settings['filters_data'][1]) >0):
        sample_list=list(map(lambda x:SampleType.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['sample_type'][x],settings['filters_data'][1]))))
        print(sample_list)
        service_matrix=list(map(lambda x: [y for y in x if len(Sample.all_objects.filter(deleted__isnull=True,request=y,sample_type__in=sample_list))>0],service_matrix))
    print(service_matrix)
    #end sample filtering

    # essay filtering
    if(len(settings['filters_data'][3])>0):
        essay_list=list(map(lambda x:Essay.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['essay'][x],settings['filters_data'][3]))))
        service_matrix=list(map(lambda x: [y for y in x if len(EssayFill.all_objects.filter(deleted__isnull=True,essay__in=essay_list,sample=y.sample))>0],service_matrix))
    print(service_matrix)
    # end essay filtering    


    # data processing
    results =[]
    for i in range(0,len(laboratory_list)):
        aux_list=[]
        aux_list.append(laboratory_list[i])
        aux_list.append(len(service_matrix[i]))
        print(i)
        try:
            aux_list.append(sum([len(x) for x in [Sample.all_objects.filter(deleted__isnull=True,request=z) for z in service_matrix[i]]])/aux_list[1])
        except:
            aux_list.append(0)
        try:
            aux_list.append(sum([x[0] for x in list(map(lambda z: [quotation_price(EssayFill.all_objects.filter(deleted__isnull=True,sample=y)) for y in Sample.all_objects.filter(deleted__isnull=True,request=z)] ,service_matrix[i])) if len(x)>0]))
        except:
            aux_list.append(0)
        if aux_list[1]>0 and aux_list[3]:
            print(aux_list[3])
            aux_list.append(aux_list[3]/aux_list[1])
            aux_list.append(sum([x.expected_duration for x in service_matrix[i]])/aux_list[1])
        else:
            aux_list.append(0)
            aux_list.append(0)
        results.append(aux_list)
    print(results)


    modal_matrix = list(map(lambda x :[[y.client.user.first_name+' '+y.client.user.last_name,  y.supervisor.user.first_name+' '+y.supervisor.user.last_name, y.state.description ,y.observations] for y in x], service_matrix))
    request.session['modal_matrix'] = modal_matrix
    request.session['modal_labels'] = ['Cliente','Supervisor','Estado','Observaciones']

    context={
        'group_type':'Laboratorio',
        'start_date':start_date,
        'end_date':end_date,
        'data_labels':table_label,
        'results':results,
        'modal_index' : -1,
        'modal_matrix' : modal_matrix
        }

    return context

def essay_group(request,context,settings):
    # Columnas
    table_label=['Tipo de Ensayo', 'Porcentaje de Uso en Servicios','Promedio de Muestras que usan el Ensayo','Costo acumulado en Servicios','Costo promedio por Servicio','Duración promedio de servicios']
    table_matrix=[]


    # Filtros

    # Essay filtering
    # essay filtering
    if(len(settings['filters_data'][3])>0):
        essay_list=list(map(lambda x:Essay.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['essay'][x],settings['filters_data'][3]))))
    else:
        essay_list=Essay.all_objects.filter(deleted__isnull=True)[::1]
    print(essay_list)

    # date filtering
    start_date=datetime.date(int(settings['start_date'][0:4]),int(settings['start_date'][5:7]),int(settings['start_date'][8:10]))
    end_date=datetime.date(int(settings['end_date'][0:4]),int(settings['end_date'][5:7]),int(settings['end_date'][8:10]))
    essay_matrix=list(map(lambda x: EssayFill.all_objects.filter(deleted__isnull=True,essay=x),essay_list))
    essay_matrix=list(map(lambda x: [y for y in x if start_date<=y.registered_date.date()<=end_date],sample_matrix))
    print(sample_matrix)
    # end date filtering
    
    # Client filtering
    if (len(settings['filters_data'][0]) >0):
        client_list=list(map(lambda x:Client.all_objects.filter(deleted__isnull=True,pk=x).first(), list(map(lambda x: settings['data_list']['client'][x],settings['filters_data'][0]))))
        sample(client_list)
        essay_matrix = list(map(lambda x : [y for y in x if y.sample.request.client in client_list],essay_matrix))
    print(essay_matrix)    
    # End Client filtering

    # Sample Type filtering
    if(len(settings['filters_data'][1]) >0):
        sample_list=list(map(lambda x:SampleType.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['sample_type'][x],settings['filters_data'][1]))))
        print(sample_list)
        essay_matrix=list(map(lambda x: [y for y in x if y.sample.sample_type in sample_list],sample_matrix))
    print(essay_matrix)
    # End Sample Type filtering

    # Laboratory filtering
    if(len(settings['filters_data'][2])>0):
        laboratory_list=list(map(lambda x:Laboratory.all_objects.filter(deleted__isnull=True,pk=x).first(),list(map(lambda x: settings['data_list']['laboratory'][x],settings['filters_data'][2]))))
        print(laboratory_list)
        essay_matrix=list(map(lambda x:[y for y in x if y.sample.request.supervisor.laboratory],essay_matrix))
    print(essay_matrix)
    # End Laboratory filtering

    # table_label=['Tipo de Ensayo', 'Porcentaje de Uso en Servicios','Promedio de Muestras que usan el Ensayo','Costo acumulado en Servicios','Costo promedio en un Servicio','Duración promedio de servicios']
    results=[]
    for i in range (0,len(essay_list)):
        aux_list=[]
        aux_list.append(essay_list[i].name)
        service_list = distinct([x.sample.request for x in essay_list[i]])
        if len(service_list)>0:
            aux_list.append(str((len(essay_matrix[i])*100/len(service_list)))+'%')
        else:
            aux_list.append('0%')
        if (len(sample_list)>0):
            aux_list.append(len(essay_matrix[i])/len(sample_list))
        else:
            aux_list.append(0)
        if (len(essay_matrix[i])>0):
            aux_list.append(sum([quotation_price(x) for x in essay_matrix[i]]))
        else:
            aux_list.append(0)
        if len(service_list)>0:
            aux_list.append((aux_list[4]/len(service_list)))
        else:
            aux_list.append(0)
        if len(service_list)>0:
            aux_list.append(sum([x.expected_duration for x in service_list])/len(service_list))
        else:
            aux_list.append(0)
        results.append(aux_list)
    print(results)
    modal_matrix = list(map(lambda x :[[y.name,y.sample.sample_type.name,y.observations] for y in x], essay_matrix))
    request.session['modal_matrix'] = modal_matrix
    request.session['modal_labels'] = ['Ensayo','Tipo de muestra','Observaciones']
    context={
        'group_type':'Laboratorio',
        'start_date':start_date,
        'end_date':end_date,
        'data_labels':table_label,
        'results':results,
        'modal_index' : -1,
        'modal_matrix' : modal_matrix
        }

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
    ##request.session['service_matrix'] = mycase[settings['criteria_list'][settings['criteria']]](context,settings)

    ##pprint(mycase[settings['criteria_list'][settings['criteria']]](context,settings))
    ##return False
    return render(request,template,mycase[settings['criteria_list'][settings['criteria']]](request,context,settings))

@ensure_csrf_cookie
def get_index(request, pk):
    ##index = request.GET['index']
    data = {
        'modal_index' : int(pk),
        'modal_matrix' : request.session.get('modal_matrix'),
        'modal_labels' : request.session.get('modal_labels')
    }

    return render(request, 'internal/reports/modal.html', data)