from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from django.urls import *
import json
from datetime import *


from internal.models import *
from internal.views.forms import *
from internal.permissions import user_passes_test
from internal.permissions.essay import *


@user_passes_test(create_essay_check, login_url='internal:index')
def create(request,
           template='internal/essay/create.html'):
    form = EssayForm(request.POST or None)
    json_form = JSONField(request.POST or None)
    list_methods = []
    list_essay_method_parameters = []
    #
    # Para los metodos
    #
    for obj in EssayMethod.all_objects.filter(deleted__isnull=True):
        my_dict = {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'methods': ' '
        }
        list_methods.append(my_dict)
    #
    # Para los parametros
    #
    for obj in EssayMethodParameter.all_objects.filter(deleted__isnull=True):
        my_dict = {
            'id': obj.id,
            'description': obj.description,
            'unit': obj.unit,
            'methods': []
        }
        methods_list = []
        query_method_list = obj.essaymethods.all().order_by('id')
        for k in range(0, len(query_method_list)):
            # print(query_method_list[k])
            methods_list.append(query_method_list[k].id)
        #print(str(obj.id)+' '+str(methods_list))
        my_dict['methods'] = methods_list
        list_essay_method_parameters.append(my_dict)
    print(list_essay_method_parameters)
    context = {'form': form,
               'list_methods': json.dumps(list_methods),
               'list_parameters': json.dumps(list_essay_method_parameters),
               'json_form': json_form}

    if request.method == 'POST':
        if form.is_valid():
            essay_saved = form.save()
            js_data = json.loads(json_form['js_data'].value())
            print(js_data)
            if js_data is not None:
                for entry in js_data:
                    print(entry)
                    method_id = entry['id']
                    print(method_id)
                    if method_id > 0:  # it wasnt created
                        EssayMethod.objects.get(
                            pk=method_id
                        ).essays.add(essay_saved)

            return redirect('internal:essay.index')
        else:
            for field in form:
                if field.errors:
                    msg = field.label + ': ' + str(field.errors)
                    messages.error(request, msg)
    return render(request, template, context)


@user_passes_test(show_essay_check, login_url='internal:index')
def show(request,
         pk,
         template='internal/essay/show.html'):
    essay = get_object_or_404(Essay.all_objects, pk=pk)
    epl = []
    methods_list = essay.essay_methods.all().order_by('id')
    for method in methods_list:
        par_id = []
        parameters_list = method.parameters.all().order_by('id')
        for parameter in parameters_list:
            par_id.append(parameter.id)
        epl.append(par_id)

    print(epl)
    context = {
        'selected_methods': methods_list,
        'parameters_list': EssayMethodParameter.all_objects.filter(
            deleted__isnull=True
        ).order_by('id'),
        'method_parameters_list': epl,
        'essay': essay
    }
    return render(request, template, context)


@user_passes_test(edit_essay_check, login_url='internal:index')
def edit(request,
         pk,
         template='internal/essay/edit.html'):
    essay = get_object_or_404(Essay, pk=pk)
    form = EssayForm(request.POST or None, instance=essay)
    json_form = JSONField(request.POST or None)
    list_methods = []
    list_essay_methods = []
    list_essay_method_parameters = []
    #
    # Para los metodos
    #
    for obj in EssayMethod.all_objects.filter(deleted__isnull=True):
        my_dict = {
            'id': obj.id,
            'name': obj.name,
            'description': obj.description,
            'methods': ' '
        }
        list_methods.append(my_dict)
    #
    # Para los parametros
    #
    for obj in EssayMethodParameter.all_objects.filter(deleted__isnull=True):
        my_dict = {
            'id': obj.id,
            'description': obj.description,
            'unit': obj.unit,
            'methods': []
        }
        methods_list = []
        query_method_list = obj.essaymethods.all().order_by('id')
        for k in range(0, len(query_method_list)):
            # print(query_method_list[k])
            methods_list.append(query_method_list[k].id)
        #print(str(obj.id)+' '+str(methods_list))
        my_dict['methods'] = methods_list
        list_essay_method_parameters.append(my_dict)

    #
    # Para los metodos pertenecientes al ensayo
    #
    aux_method_list = essay.essay_methods.all().order_by('id')
    for obj in aux_method_list:
        list_essay_methods.append(obj.id)

    context = {
        'form': form,
        'list_methods': json.dumps(list_methods),
        'list_parameters': json.dumps(list_essay_method_parameters),
        'json_form': json_form,
        'list_essay_methods': list_essay_methods,
        'pk': pk,
        'essay': essay
    }
    if request.method == 'POST':
        if form.is_valid():
            essay_saved = form.save()
            js_data = json.loads(json_form['js_data'].value())
            print(js_data)
            if js_data is not None:
                entry_id_list = []
                for entry in js_data:
                    print(entry)
                    method_id = entry['id']
                    entry_id_list.append(method_id)
                    print(method_id)
                    if not(method_id in list_essay_methods):  # it is new
                        EssayMethod.objects.get(
                            pk=method_id).essays.add(essay_saved)
                for obj_id in list_essay_methods:
                    if not(obj_id in entry_id_list):
                        essay.essay_methods.remove(
                            EssayMethod.objects.get(pk=obj_id))
            return redirect('internal:essay.index')
        else:
            for field in form:
                if field.errors:
                    msg = field.label + ': ' + str(field.errors)
                    messages.error(request, msg)
    return render(request, template, context)


@user_passes_test(show_essay_check, login_url='internal:index')
def index(request,
          template='internal/essay/index.html',
          extra_context=None):
    essays = Essay.all_objects.order_by('name')

    context = {
        'essay_list': essays,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(delete_essay_check, login_url='internal:index')
def delete(request, pk):
    essay = get_object_or_404(Essay, pk=pk)
    essay.delete()

    return redirect('internal:essay.index')
