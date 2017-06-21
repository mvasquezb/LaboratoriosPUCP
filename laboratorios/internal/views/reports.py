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
    # First criteria is range of dates, which doesnt need any from db
    # Second criteria is client, which we do have
    client_list = Client.all_objects.filter(deleted__isnull=True)
    
    # Third  criteria is sample type, which we also have
    sample_type_list = SampleType.all_objects.filter(deleted__isnull=True)

    # Should be also clear that laboratory must be a criteria
    laboratory_list = Laboratory.all_objects.filter(deleted__isnull=True)

    # as we do not want to mantain later the logic bc of more fitlers,
    # lets use a dictionary

    # Because we wont always check for all criterias, we should have a
    # register which expose so

    # criteria_selection = {
            #     'client':False,
            #     'sample_type':False,
            #     'laboratory':False,
            # }
    criteria_selection = [
        'client',
        'sample_type',
        'laboratory'
        ]

    criteria_selection_string={
        'client':'Cliente',
        'sample_type':'Tipo de Muestra',
        'laboratory':'Laboratorio',
    }

    # The JSONField wil pickup the following:
    # 1.- Date Range
    # 2.- Dictionary of selected criteria
    # 3.- Expected type of report and chart -- to be seen lmao
    # 4.- Criteria selection structure, as context itself is immutable
    json_form = JSONField(request.POST or None)

    context = {
        'criteria':criteria_selection,
        'criteria_string':criteria_selection_string,
        'clients':client_list,
        'sample_types':sample_type_list,
        'laboratories':laboratory_list,
        }
    if request == 'POST' and 'js_data' in request.body:
        ## processing of shit right here
        js_data = json.loads(json_form['js_data'].value())
        if js_data is not None:
            criteria_string = js_data['date_range'][0] + '%' + js_data['date_range'][1]
            for i in range(0,len(criteria_selection)):
                if (i==0):
                    criteria_string = criteria_string + '%'
                criteria = criteria_selection[i]
                criteria_string = criteria_string + criteria
                if js_data['criteria'][criteria] == True:
                    criteria_string = criteria_string + '%' + '1' + '%' + js_data[criteria]
                else:
                    criteria_string = criteria_string + '%' + '0'
                if i < (len(criteria_selection)-1):
                    criteria_string=criteria_string+'%'
        ## end of processing shit
        ## passing string with selections to processing template
            return redirect(reverse('internal:reports.results',criteria_string))
    return render(request,template,context)


def processing_parameters(
    request,
    criteria_string,
    template='internal/reports/results.html'
    ):
    print(criteria_string)
    context={}

    return render(request,template,context)