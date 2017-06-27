from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count
from django.http import JsonResponse
from django.http import HttpResponse

from internal.models import *
from .forms import LaboratoryForm

import json as simplejson
from datetime import timedelta
from internal.permissions import user_passes_test
from internal.permissions.laboratory import *


@user_passes_test(index_laboratory_check, login_url='internal:index')
def index(request,
          template='internal/laboratory/index.html',
          extra_context=None):
    laboratorys = Laboratory.all_objects.all()
    context = {
        'laboratorys_list': laboratorys
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def inventory_modal(request):
    if request.method == 'GET' and request.is_ajax():
        # print("LLEGA BIEN AL VIEW")
        dicc = dict(request.GET)
        inventory_pk = dicc['inventory_pk'][0]
        # print(inventory_pk)
        inventory = Inventory.all_objects.get(pk=inventory_pk)
        article_inventory = ArticleInventory.all_objects.filter(
            inventory=inventory)
        matches_list = []
        for match in article_inventory:
            article_name = match.article.name
            article_quantity = match.article.quantity
            matches_list.append((article_name, article_quantity))
        data = {
            'inventory_name': inventory.name,
            'inventory_location': inventory.location,
            'inventory_type': inventory.inventory_type,
            'inventory_matches': matches_list
        }
        return JsonResponse(data)
    return HttpResponse("GG")


def services_index(request,
                   pk):
    if request.method == 'POST' and request.is_ajax():
        dicc = dict(request.POST)
        priorities_pk = dicc['priorities_pk[]']
        services_pk = dicc['services_pk[]']
        for i in range(0, len(services_pk)):
            if services_pk[i] and priorities_pk[i] and priorities_pk[i] != -1:
                service = ServiceRequest.all_objects.get(
                    deleted__isnull=True,
                    pk=services_pk[i]
                )
                service.priority = ServiceRequestPriority.all_objects.get(
                    deleted__isnull=True,
                    pk=priorities_pk[i]
                )
                service.save()
    laboratory = get_object_or_404(
        Laboratory.all_objects,
        pk=pk
    )
    all_priorities = ServiceRequestPriority.all_objects.filter(
        deleted__isnull=True)
    laboratory_services = ServiceRequest.all_objects.filter(
        deleted__isnull=True,
        supervisor__in=laboratory.employees.all()
    )

    # get data for track service's graphic
    month_names = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre'
    ]

    # get only services of the current laboratory
    service_request_list = laboratory_services

    my_data = []
    now = timezone.localtime(timezone.now())
    for i in range(0, len(service_request_list)):
        date_in_service = service_request_list[i].registered_date
        # date_in_service.strftime("%d/%m/%Y")
        # date_in_service.replace(day=date_in_service.day+service_request_list[i].expected_duration).strftime("%d/%m/%Y")

        # progresion calculation
        expected_duration = service_request_list[i].expected_duration
        delta = now - date_in_service
        total = 100 * delta.days / expected_duration
        total = int(total)
        end_date = date_in_service + timedelta(days=expected_duration)
        client = service_request_list[i].client

        my_dict = {
            "id": service_request_list[i].id,
            "title": "Cliente " + client.user.get_full_name(),
            "start_date": date_in_service.strftime("%m/%d/%Y"),
            "end_date": end_date.strftime("%m/%d/%Y"),
            "value": 67,
            "term": "Short Term",
            "completion_percentage": total,
            "color": "#770051",
        }
        my_data.append(my_dict)
    js_data = simplejson.dumps(my_data)

    context = {
        'js_data': js_data,
        'actual_month': month_names[now.month - 1] + " " + str(now.year),
        'laboratory_services': laboratory_services,
        'laboratory': laboratory,
        'priorities': all_priorities
    }
    template = 'internal/laboratory/services_index.html'
    return render(request, template, context)


@user_passes_test(create_laboratory_check, login_url='internal:index')
def create(request,
           template='internal/laboratory/create.html',
           extra_content=None):
    form = LaboratoryForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            # here we add essay_methods to every employee of the new laboratory
            for employee in form.cleaned_data['employees']:
                for essay_method in form.cleaned_data['essay_methods']:
                    employee.essay_methods.add(essay_method)
                employee.save()
            form.save()
            messages.success(
                request, 'Se ha creado un nuevo laboratorio exitosamante!')
            return redirect('internal:laboratory.index')
        else:
            print(form.errors)
            for field, errors in form.errors.items():
                if (field == "name") and list(errors) == ['Ya existe Laboratory con este Name.']:
                    messages.error(
                        request, 'Este nombre de laboratorio ya existe, pruebe otro')
                    return redirect('internal:laboratory.create')

            # return HttpResponse(form.errors)
    else:
        # users =
        # Employee.all_objects.filter(deleted__isnull=True,laboratories__isnull=True)
        # #just active users
        users = Employee.all_objects.annotate(
            labs=Count('laboratories')
        ).filter(
            Q(labs=0),
            deleted__isnull=True,
        )
        inventories = Inventory.all_objects.filter(deleted__isnull=True)
        essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        context = {
            'users': users,
            'inventories': inventories,
            'essaymethods': essaymethods,
            'form': form,
        }
        return render(request, template, context)


@user_passes_test(edit_laboratory_check, login_url='internal:index')
def edit(request,
         pk):
    if request.method == 'POST':
        instance = Laboratory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        aux_form = LaboratoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            # here we add essay_methods to every employee of the new laboratory
            for employee in aux_form.cleaned_data['employees']:
                essay_methods = aux_form.cleaned_data['essay_methods']
                employee.essay_methods.add(*essay_methods)
                employee.save()
            aux_form.save()
            messages.success(
                request, 'Se ha editado el laboratorio exitosamante')
            return redirect('internal:laboratory.index')
        else:
            messages.error(
                request, 'Ya existe un laboratorio con el mismo nombre, ingrese otro')
            # return HttpResponse(status=204)
            return redirect('internal:laboratory.edit', pk=pk)
    else:
        laboratory = Laboratory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        #
        all_users = Employee.all_objects.annotate(
            labs=Count('laboratories')
        ).filter(
            # Get employees that do not belong to a laboratory
            # Or that belong to this laboratory
            Q(labs=0) | Q(laboratories=laboratory.id),
            deleted__isnull=True,
        )
        selected_users = laboratory.employees.all()
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {
            'laboratory': laboratory,
            'users': all_users,
            'selected_users': selected_users,
            'inventories': all_inventories,
            'selected_inventories': selected_inventories,
            'essaymethods': all_essaymethods,
            'selected_essaymethods': selected_essaymethods,
            'form': form
        }
        template = 'internal/laboratory/edit.html'
        return render(request, template, context)


@user_passes_test(delete_laboratory_check, login_url='internal:index')
def delete(request, pk):
    laboratory = get_object_or_404(Laboratory, pk=pk)
    laboratory.delete()
    messages.success(request, 'Se ha borrado el laboratorio existosamente')
    return redirect('internal:laboratory.index')


@user_passes_test(show_laboratory_check, login_url='internal:index')
def show(request,
         pk):
    if request.method == 'POST':
        instance = Laboratory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        aux_form = LaboratoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
            aux_form.save()
            return redirect('internal:laboratory.index')
    else:
        laboratory = Laboratory.all_objects.get(
            pk=pk
        )
        #
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = laboratory.employees.all()
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {
            'laboratory': laboratory,
            'all_users': all_users,
            'selected_users': selected_users,
            'all_inventories': all_inventories,
            'selected_inventories': selected_inventories,
            'all_essaymethods': all_essaymethods,
            'selected_essaymethods': selected_essaymethods,
            'form': form
        }
        template = 'internal/laboratory/show.html'
        return render(request, template, context)


def track_services(request, pk,
                   template=('internal/laboratory/' +
                             'track_services.html')):
    month_names = [
        'Enero',
        'Febrero',
        'Marzo',
        'Abril',
        'Mayo',
        'Junio',
        'Julio',
        'Agosto',
        'Septiembre',
        'Octubre',
        'Noviembre',
        'Diciembre'
    ]

    # get only services of the current laboratory
    all_services = ServiceRequest.all_objects.all(deleted__isnull=True)
    laboratory = Laboratory.all_objects.get(deleted__isnull=True, pk=pk)
    all_employes = laboratory.employees.all()
    service_request_list = []
    for service in all_services:
        service_supervisor = service.supervisor
        for employee in all_employes:
            if (employee == service_supervisor):
                service_request_list.append(service)
                break
    #
    my_data = []
    now = timezone.localtime(timezone.now())
    for i in range(0, len(service_request_list)):
        date_in_service = service_request_list[i].registered_date
        # date_in_service.strftime("%d/%m/%Y")
        # date_in_service.replace(day=date_in_service.day+service_request_list[i].expected_duration).strftime("%d/%m/%Y")

        # progresion calculation
        expected_duration = service_request_list[i].expected_duration
        delta = now - date_in_service
        total = 100 * delta.days / expected_duration
        total = int(total)
        end_date = date_in_service.replace(
            day=date_in_service.day + expected_duration
        )
        client = service_request_list[i].client

        my_dict = {
            "id": service_request_list[i].id,
            "title": "Cliente " + client.user.get_full_name(),
            "start_date": date_in_service.strftime("%m/%d/%Y"),
            "end_date": end_date.strftime("%m/%d/%Y"),
            "value": 67,
            "term": "Short Term",
            "completion_percentage": total,
            "color": "#770051",
        }
        my_data.append(my_dict)
    js_data = simplejson.dumps(my_data)
    context = {
        'js_data': js_data,
        'actual_month': month_names[now.month - 1] + " " + str(now.year),
        'laboratory': laboratory
    }
    return render(request, template, context)
