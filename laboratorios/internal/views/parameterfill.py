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

def fill_parameters(request,
        pk,
        template='internal/parameterfill/fill_parameters.html'):
    method = EssayMethodFill.all_objects.get(deleted__isnull=True,pk=pk)
    sample = method.essay.sample
    parameter_list=method.parameters.all().order_by('id')
    parameter_form_list=[]
    for i in range(0,len(parameter_list)):
        parameter_form_list.append(ParameterValueForm(request.POST or None,
                                                                    instance=parameter_list[i],
                                                                    prefix='emf_' + str(parameter_list[i].pk)))
    context={
        'sample':sample,
        'method':method,
        'parameter_forms':parameter_form_list,
        'pk':pk,
    }
    if request.method == 'POST':
        # verificacion
        forms_verified = 0  # Means true lol
        # loop for verifying each essay method form
        for i in range(0, len(parameter_form_list)):
            if parameter_form_list[i].is_valid():
                pass
            else:
                forms_verified += 1
        # end of verifying segment

        if forms_verified == 0:
            # add save for each form
            for i in range(0, len(parameter_form_list)):
                    parameter_form_list[i].save()
            return redirect(reverse("internal:index"))
    return render(request,template,context)
    

    