from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from django.http import HttpResponse
from django.utils import timezone

from internal.models import *
from .forms import LaboratoryForm
import json as simplejson


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
        Laboratory.all_objects.filter(deleted__isnull=True),
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
        'laboratory_services': laboratory_services,
        'laboratory': laboratory,
        'priorities': all_priorities
    }
    template = 'internal/laboratory/services_index.html'
    return render(request, template, context)


def create(request,
           template='internal/laboratory/create.html',
           extra_content=None):
    if request.method == 'POST':
        form = LaboratoryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Se ha creado un nuevo laboratorio exitosamante!')
            return redirect('internal:laboratory.index')
        else:
            # print(form.errors)
            for field, errors in form.errors.items():
                if (field == "name") and list(errors) == ['Ya existe Laboratory con este Name.']:
                    messages.error(
                        request, 'Este nombre de laboratorio ya existe, pruebe otro')
                    return redirect('internal:laboratory.create')

            # return HttpResponse(form.errors)
    else:
        users = Employee.all_objects.filter(deleted__isnull=True)
        service_hours = LaboratoryServiceHours.all_objects.filter(
            deleted__isnull=True
        )
        inventories = Inventory.all_objects.filter(deleted__isnull=True)
        essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        form = LaboratoryForm()
        context = {
            'users': users,
            'service_hours': service_hours,
            'inventories': inventories,
            'essaymethods': essaymethods,
            'form': form
        }
        return render(request, template, context)


def edit(request,
         pk):
    if request.method == 'POST':
        instance = Laboratory.all_objects.get(
            deleted__isnull=True,
            pk=pk
        )
        aux_form = LaboratoryForm(request.POST or None, instance=instance)
        if aux_form.is_valid():
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
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = laboratory.employees.all()
        #
        all_service_hours = LaboratoryServiceHours.all_objects.filter(
            deleted__isnull=True
        )
        selected_service_hours = laboratory.service_hours
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {'laboratory': laboratory, 'all_users': all_users,
                   'selected_users': selected_users, 'all_service_hours': all_service_hours,
                   'selected_service_hours': selected_service_hours,
                   'all_inventories': all_inventories, 'selected_inventories': selected_inventories,
                   'all_essaymethods': all_essaymethods, 'selected_essaymethods': selected_essaymethods,
                   'form': form}
        template = 'internal/laboratory/edit.html'
        return render(request, template, context)


def delete(request, pk):
    laboratory = get_object_or_404(Laboratory, pk=pk)
    laboratory.delete()
    messages.success(request, 'Se ha borrado el laboratorio existosamente')
    return redirect('internal:laboratory.index')


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
            deleted__isnull=True,
            pk=pk
        )
        #
        all_users = Employee.all_objects.filter(deleted__isnull=True)
        selected_users = laboratory.employees.all()
        #
        all_service_hours = LaboratoryServiceHours.all_objects.filter(
            deleted__isnull=True
        )
        selected_service_hours = laboratory.service_hours
        #
        all_inventories = Inventory.all_objects.filter(deleted__isnull=True)
        selected_inventories = laboratory.inventory.all()
        #
        all_essaymethods = EssayMethod.all_objects.filter(deleted__isnull=True)
        selected_essaymethods = laboratory.essay_methods.all()
        #
        form = LaboratoryForm()
        context = {'laboratory': laboratory, 'all_users': all_users,
                   'selected_users': selected_users, 'all_service_hours': all_service_hours,
                   'selected_service_hours': selected_service_hours,
                   'all_inventories': all_inventories, 'selected_inventories': selected_inventories,
                   'all_essaymethods': all_essaymethods, 'selected_essaymethods': selected_essaymethods,
                   'form': form}
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
