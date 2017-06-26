from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.urls import *
import json
from datetime import *

from internal.models import *
from internal.views.forms import *
from django.contrib.auth.decorators import user_passes_test
from internal.permissions.essayMethod import *


@user_passes_test(create_essay_method_check, login_url='internal:index')
def create(request,
           template='internal/essaymethod/create.html'):
    form = EssayMethodForm(request.POST or None)
    json_form = JSONField(request.POST or None)
    list_essay_method_parameters = []
    #
    # Para los parametros
    #
    for obj in EssayMethodParameter.all_objects.filter(deleted__isnull=True):
        my_dict = {
            'id': obj.id,
            'description': obj.description,
            'unit': obj.unit
        }
        list_essay_method_parameters.append(my_dict)
    print(EssayMethodParameter.all_objects.filter(deleted__isnull=True))
    context = {'form': form,
               'list_parameters': json.dumps(list_essay_method_parameters),
               'json_form': json_form}

    if request.method == 'POST':
        if form.is_valid():
            essaymethod_saved = form.save()
            js_data = json.loads(json_form['js_data'].value())
            print(js_data)
            if js_data is not None:
                existing_data = js_data['existing_data']
                for entry in existing_data:
                    print(entry)
                    parameter_id = entry['id']
                    print(parameter_id)
                    EssayMethodParameter.objects.get(
                        pk=parameter_id).essaymethods.add(essaymethod_saved)
                created_data = js_data['created_data']
                for entry in created_data:
                    parameter_obj = EssayMethodParameter(
                        description=entry['description'], unit=entry['unit'])
                    parameter_obj.save()
                    parameter_obj.essaymethods.add(essaymethod_saved)
                    parameter_obj.save()
            return redirect('internal:essaymethod.index')
    return render(request, template, context)


@user_passes_test(edit_essay_method_check, login_url='internal:index')
def edit(request,
         pk,
         template='internal/essaymethod/edit.html'):
    essay_method = EssayMethod.objects.get(pk=pk)
    form = EssayMethodForm(request.POST or None, instance=essay_method)
    json_form = JSONField(request.POST or None)
    list_essay_method_parameters = []
    list_method_parameters = []
    #
    # Para los parametros
    #
    essaymethod_parameters = EssayMethodParameter.all_objects.filter(
        deleted__isnull=True
    ).order_by('id')
    for obj in essaymethod_parameters:
        my_dict = {
            'id': obj.id,
            'description': obj.description,
            'unit': obj.unit
        }
        list_essay_method_parameters.append(my_dict)
        if obj in essay_method.parameters.all():
            list_method_parameters.append(my_dict['id'])
    print(EssayMethodParameter.all_objects.filter(deleted__isnull=True))
    context = {
        'form': form,
        'list_parameters': json.dumps(list_essay_method_parameters),
        'list_selected_parameters': json.dumps(list_method_parameters),
        'json_form': json_form,
        'pk': pk,
        'essay_method': essay_method,
    }

    if request.method == 'POST':
        print(form.is_valid())
        if form.is_valid():
            essaymethod_saved = form.save()
            js_data = json.loads(json_form['js_data'].value())
            print(js_data)
            if js_data is not None:
                existing_data = js_data['existing_data']
                aux_existing_id = []
                for entry in existing_data:
                    print(entry)
                    parameter_id = entry['id']
                    aux_existing_id.append(parameter_id)
                    print(parameter_id)
                    EssayMethodParameter.objects.get(
                        pk=parameter_id).essaymethods.add(essaymethod_saved)
                for param_id in list_method_parameters:
                    if not(param_id in aux_existing_id):
                        obj_par = EssayMethodParameter.objects.get(pk=param_id)
                        essay_method.parameters.remove(obj_par)
                created_data = js_data['created_data']
                for entry in created_data:
                    parameter_obj = EssayMethodParameter(
                        description=entry['description'], unit=entry['unit'])
                    parameter_obj.save()
                    parameter_obj.essaymethods.add(essaymethod_saved)
                    parameter_obj.save()
            return redirect('internal:essaymethod.index')
    return render(request, template, context)


@user_passes_test(show_essay_method_check, login_url='internal:index')
def show(request,
         pk,
         template='internal/essaymethod/show.html'):
    essaymethod = get_object_or_404(EssayMethod, pk=pk)
    parameters_list = essaymethod.parameters.all().order_by('id')
    context = {
        'selected_parameters': parameters_list,
        'essaymethod': essaymethod,
        'pk': pk,
    }
    return render(request, template, context)


@user_passes_test(index_essay_method_check, login_url='internal:index')
def index(request,
          template='internal/essaymethod/index.html',
          extra_context=None):
    essaymethods = EssayMethod.objects.order_by('name')

    context = {
        'essaymethod_list': essaymethods,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(delete_essay_method_check, login_url='internal:index')
def delete(request, pk):
    essaymethod = get_object_or_404(EssayMethod, pk=pk)
    essaymethod.delete()

    return redirect('internal:essaymethod.index')
