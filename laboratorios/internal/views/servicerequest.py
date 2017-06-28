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
from django.http import JsonResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone
# from django.conf import settings
# from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.template.loader import get_template

from internal.models import *
from internal.views.forms import *
from internal import utils

from io import BytesIO
from xhtml2pdf import pisa
import json as simplejson
from datetime import datetime, timedelta
from internal.permissions import user_passes_test
from functools import reduce
from internal.permissions.serviceRequest import *


@user_passes_test(index_service_request_check, login_url='internal:index')
def index(request,
          template='internal/servicerequest/index.html',
          extra_context=None):
    context = {
        'requests': ServiceRequest.all_objects.filter(deleted__isnull=True)
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(create_service_request_check, login_url='internal:index')
def create(request,
           pk,
           template='internal/servicerequest/create.html'):
    selected_client = Client.all_objects.get(pk=pk)
    service_request_form = ServiceRequestCreateForm(
        request.POST or None,
        initial={
            'client': selected_client
        }
    )
    context = {
        'sr_form': service_request_form,
        'pk': pk
    }
    if request.method == 'POST':
        if service_request_form.is_valid():
            created_service_request = service_request_form.save(commit=False)
            messages.success(
                request,
                'Se ha creado la solicitud exitosamante!'
            )
            # creating an initial state if not existing yet
            init_state = ServiceRequestState.all_objects.filter(
                deleted__isnull=True,
                slug='initial'
            ).first()
            if init_state is None:
                init_state = ServiceRequestState(
                    slug='initial',
                    description='Estado Inicial'
                )
                init_state.save()
            created_service_request.state = init_state
            created_service_request.save()
            return redirect(reverse('internal:servicerequest.index'))
    return render(request, template, context)


def select_client(request,
                  template='internal/servicerequest/select_client.html'):
    clients = Client.all_objects.filter(
        deleted__isnull=True
    ).order_by('doc_number', 'user__username')
    context = {'client_list': clients}
    return render(request, template, context)


def create_client(request,
                  template='internal/servicerequest/create_client.html'):
    user_form = UserCreationForm(request.POST or None)
    form = ClientForm(request.POST or None)
    context = {
        'form': form,
        'user_form': user_form,
    }
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            new_client = form.save()
            return redirect('internal:servicerequest.create', new_client.pk)
        else:
            # Show errors
            print(user_form.errors, form.errors)
            pass
    return render(request, template, context)


@user_passes_test(edit_service_request_check, login_url='internal:index')
def edit(request,
         pk,
         template='internal/servicerequest/edit.html'):
    service_request = ServiceRequest.all_objects.get(pk=pk)

    service_request_form = ServiceRequestForm(
        request.POST or None, instance=service_request)
    # For all samples and their selected essayFills in list
    sample_list = Sample.all_objects.filter(
        deleted__isnull=True,
        request=service_request
    )
    essay_fill_list = []
    essay_methods_list = []  # To get all essay_methods for every sample
    essay_methods_chosen_forms = []  # To get whether each essay_method is chosen or not

    for i in range(0, len(sample_list)):
        sample_listed = sample_list[i]
        essay_fill = EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample=sample_listed
        ).first()

        essay_fill_list.append(essay_fill)
        essay_methods_list.append(
            EssayMethodFill.all_objects.filter(
                deleted__isnull=True,
                essay=essay_fill
            )
        )
        aux_essay_methods_forms = []
        for j in range(0, len(essay_methods_list[i])):
            aux_essay_methods_forms.append(
                EssayMethodFillChosenForm(
                    request.POST or None,
                    instance=essay_methods_list[i][j],
                    prefix='emf_' + str(essay_methods_list[i][j].pk)
                )
            )
        essay_methods_chosen_forms.append(aux_essay_methods_forms)

    context = {
        'form': service_request_form,
        'service_request': service_request,
        'samples': sample_list,
        'essays': essay_fill_list,
        'essays_methods': essay_methods_list,
        'essay_methods_chosen_forms': essay_methods_chosen_forms,
        'pk': pk,
        'clients': Client.all_objects.filter(deleted__isnull=True),
        'employees': Employee.all_objects.filter(deleted__isnull=True),
        'states': ServiceRequestState.all_objects.filter(deleted__isnull=True),
        'external_providers': ExternalProvider.all_objects.filter(
            deleted__isnull=True
        )
    }

    # verificacion
    forms_verified = 0  # Means true lol

    # loop for verifying each essay method form
    for i in range(0, len(essay_methods_chosen_forms)):
        for j in range(0, len(essay_methods_chosen_forms[i])):
            if essay_methods_chosen_forms[i][j].is_valid():
                pass
            else:
                forms_verified += 1
    if service_request_form.is_valid():
        pass
    else:
        forms_verified += 1
    # end of verifying segment

    if forms_verified == 0:
        service_request_form.save()
        # add save for each form
        for i in range(0, len(essay_methods_chosen_forms)):
            for j in range(0, len(essay_methods_chosen_forms[i])):
                print(essay_methods_chosen_forms[i][j].save().chosen)
                essay_methods_chosen_forms[i][j].save()
        return redirect(reverse("internal:servicerequest.index"))
    return render(request, template, context)


def add_sample(request,
               pk,
               template='internal/servicerequest/add_sample.html'):
    service_request = ServiceRequest.all_objects.get(pk=pk)
    sample_form = SampleForm(
        request.POST or None,
        initial={
            'request': service_request,
        }
    )
    context = {
        'form': sample_form,
        'pk': pk
    }
    # verificacion
    if request.method == 'POST':
        if sample_form.is_valid():
            sample_form.save()
            return redirect('internal:servicerequest.edit', pk)
        else:
            context['errors'] = str(sample_form.errors)
    return render(request, template, context)


def edit_sample(request,
                pk_request,
                pk_sample,
                template='internal/servicerequest/edit_sample.html'):
    sample = Sample.all_objects.get(pk=pk_sample)
    sample_form = SampleEditForm(request.POST or None, instance=sample)
    essay_fill_form = EssayFillSelectionForm(
        request.POST or None,
        instance=EssayFill.all_objects.get(sample=sample)
    )
    forms = [sample_form, essay_fill_form]
    context = {
        'forms': forms,
        'pk_request': pk_request,
        'pk_sample': pk_sample
    }
    if sample_form.is_valid() and essay_fill_form.is_valid():
        sample_form.save()
        essay_fill_form.save()
        return redirect('internal:servicerequest.edit', pk_request)
    return render(request, template, context)


@user_passes_test(delete_service_request_check, login_url='internal:index')
def delete(request,
           pk):
    service_request = ServiceRequest.all_objects.get(pk=pk)
    service_request.delete()

    return redirect(reverse("internal:servicerequest.index"))


def delete_sample(request,
                  pk_request,
                  pk_sample):
    sample = Sample.all_objects.get(pk=pk_sample)
    sample.delete()

    return redirect('internal:servicerequest.edit', pk_request)


@user_passes_test(show_service_request_check, login_url='internal:index')
def show(request,
         pk,
         template='internal/servicerequest/show.html'):
    service_request = ServiceRequest.all_objects.get(pk=pk)
    service_request_form = ServiceRequestForm(
        request.POST or None, instance=service_request)
    # For all samples and their selected essayFills in list
    sample_list = Sample.all_objects.filter(
        deleted__isnull=True,
        request=service_request
    )
    essay_fill_list = []
    essay_methods_list = []  # To get all essay_methods for every sample
    essay_methods_chosen_forms = []  # To get whether each essay_method is chosen or not

    for i in range(0, len(sample_list)):
        sample_listed = sample_list[i]
        essay_fill = EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample=sample_listed
        ).first()

        essay_fill_list.append(essay_fill)
        essay_methods_list.append(
            EssayMethodFill.all_objects.filter(
                deleted__isnull=True,
                essay=essay_fill
            )
        )
        aux_essay_methods_forms = []
        for j in range(0, len(essay_methods_list[i])):
            aux_essay_methods_forms.append(
                EssayMethodFillChosenForm(
                    request.POST or None,
                    instance=essay_methods_list[i][j],
                    prefix='emf_' + str(essay_methods_list[i][j].pk)
                )
            )
        essay_methods_chosen_forms.append(aux_essay_methods_forms)

    context = {
        'form': service_request_form,
        'service_request': service_request,
        'samples': sample_list,
        'essays': essay_fill_list,
        'essays_methods': essay_methods_list,
        'essay_methods_chosen_forms': essay_methods_chosen_forms,
        'pk': pk,
        'clients': Client.all_objects.filter(deleted__isnull=True),
        'employees': Employee.all_objects.filter(deleted__isnull=True),
        'states': ServiceRequestState.all_objects.filter(deleted__isnull=True),
        'external_providers': ExternalProvider.all_objects.filter(
            deleted__isnull=True
        )
    }
    # verificacion
    forms_verified = 0  # Means true lol

    # loop for verifying each essay method form
    for i in range(0, len(essay_methods_chosen_forms)):
        for j in range(0, len(essay_methods_chosen_forms[i])):
            if essay_methods_chosen_forms[i][j].is_valid():
                pass
            else:
                forms_verified += 1
    if service_request_form.is_valid():
        pass
    else:
        forms_verified += 1
    # end of verifying segment

    if forms_verified == 0:
        service_request_form.save()
        # add save for each form
        for i in range(0, len(essay_methods_chosen_forms)):
            for j in range(0, len(essay_methods_chosen_forms[i])):
                print(essay_methods_chosen_forms[i][j].save().chosen)
                essay_methods_chosen_forms[i][j].save()
        return redirect(reverse("internal:servicerequest.index"))
    return render(request, template, context)


def quotation(request,
              request_id,
              template='internal/servicerequest/quotation.html',
              extra_context=None):
    service_request = get_object_or_404(
        ServiceRequest.all_objects, pk=request_id)
    quotation, created = Quotation.all_objects.get_or_create(
        request=service_request
    )
    essay_list = EssayFill.all_objects.filter(
        sample__in=service_request.sample_set.all(),
    )
    quotation_essays = quotation.essay_fills.all()
    essays_to_add = set(essay_list) - set(quotation_essays)
    quotation.essay_fills.add(*essays_to_add)

    essay_list = quotation.essay_fills.all()
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
    context = {
        'service_request': service_request,
        'essay_list': essay_list,
        'total_price': total_price,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@ensure_csrf_cookie
def assign_employee(request,
                    request_id,
                    sample_id,
                    template='internal/servicerequest/assign_employee.html',
                    extra_context=None):
    if request.method == 'GET':
        essay_methods = request.GET.get('methods', '')
    elif request.method == 'POST':
        essay_methods = request.POST.get('methods', '')

    try:
        essay_methods = simplejson.loads(essay_methods)
    except simplejson.decoder.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'errors': 'Ocurrió un error al procesar su solicitud'
        }, json_dumps_params={'ensure_ascii': False})

    essay_methods = {
        em['id']: em['checked']
        for em in essay_methods
    }
    chosen_ems = {
        id: checked
        for id, checked in essay_methods.items() if checked
    }
    service_request = get_object_or_404(
        ServiceRequest.all_objects.filter(deleted__isnull=True),
        pk=request_id
    )
    sample = get_object_or_404(service_request.sample_set.all(), pk=sample_id)
    essay_method_list = EssayMethodFill.all_objects.filter(
        pk__in=list(essay_methods.keys()),
    )
    chosen_ems = EssayMethodFill.all_objects.filter(
        deleted__isnull=True,
        pk__in=chosen_ems.keys()
    )

    employee_q = Q()
    for essay_method in chosen_ems:
        employee_q &= Q(essay_methods=essay_method.essay_method)
    employee_list = Employee.all_objects.filter(
        # employee_q,
        deleted__isnull=True
    )

    form = ServiceAssignEmployeeForm(
        request.POST or None,
        employee=employee_list
    )

    query = Q()
    for essay_method in chosen_ems:
        query &= Q(assigned_essay_methods__in=[essay_method])

    if query:
        assigned_employee = employee_list.filter(query).first()
    else:
        assigned_employee = None
    print(assigned_employee)
    # Está cagada esta lógica
    if request.method == 'POST':
        if form.is_valid():
            # Save essay method fill
            print(essay_method_list)
            for em in essay_method_list:
                print(em, em.id, essay_methods[em.pk])
                em.chosen = essay_methods[em.id]
                em.save()
            # Remove previous assigned employee, if existant
            if assigned_employee:
                assigned_employee.assigned_essay_methods.remove(*chosen_ems)
            employee = form.cleaned_data['employee']
            print(employee)
            emp_methods = employee.assigned_essay_methods.all()
            methods_to_add = set(chosen_ems) ^ set(emp_methods)
            print(methods_to_add)
            employee.assigned_essay_methods.set(methods_to_add)
            print(EssayMethodFill.all_objects.filter(employees=employee))

            if request.is_ajax():
                return JsonResponse({
                    'success': True,
                    'message': 'Se asignó la muestra correctamente',
                    'redirect': reverse(
                        'internal:servicerequest.edit',
                        args=(service_request.id,)
                    ),
                }, json_dumps_params={
                    'ensure_ascii': False,
                })
        else:
            if request.is_ajax():
                return JsonResponse({
                    'success': False,
                    'errors': str(form.errors),
                }, json_dumps_params={
                    'ensure_ascii': False,
                })
    context = {
        'employees': employee_list,
        'service_request': service_request,
        'sample': sample,
        'essay_methods': essay_method_list,
        'form': form,
        'assigned_employee': assigned_employee,
    }
    return render(request, template, context)


# Agregado
def approve(request,
            pk, template='internal/servicerequest/index.html'):
    service_request = ServiceRequest.all_objects.get(pk=pk)
    state = ServiceRequestState.all_objects.get(description="Aprobado")
    service_request.state = state  # Le asignamos el estado de aprobado
    service_request.save()
    client = Client.all_objects.get(pk=service_request.client.id)

    service_contract = ServiceContract(
        client=client,
        request=service_request
    )
    service_contract.save()
    messages.success(request, 'Se ha aprobado la solicitud exitosamante!')
    return redirect('internal:servicerequest.index')
    # return redirect(reverse("internal:servicerequest.index"))


def workload_view_per_request(request,
                              template='internal/servicerequest/' +
                                       'workload_view_per_request.html'):
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
    service_request_list = ServiceRequest.all_objects.filter(
        deleted__isnull=True
    )
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
        'actual_month': month_names[now.month - 1] + " " + str(now.year)
    }
    return render(request, template, context)

def validate_name(name):
    if (name.upper() in ['.','..','CON','PRN','AUX','CLOCK$','NUL','COM1','COM2','COM3','COM4','COM5','COM6','COM7','COM8','COM9','LPT1','LPT2','LPT3','LPT4','LPT5','LPT6','LPT7','LPT8','LPT9','LST','KEYBD$','SCREEN$','$IDLE$','CONFIG$']):
        return False
    for c in name:
        if (not c.isalnum()) and (not c in ['_', ' ', '-', '&', '(',')', '$']):
            return False
    if (name[-1] == '.'):
        return False
    return True


def upload(request, id):
    sr_object = get_object_or_404(
        ServiceRequest,
        pk=id
    )
    if request.method == 'POST':
        myfile = request.FILES.get('myfile')
        if not myfile:
            messages.error(request, 'Debe seleccionar un archivo')
            return redirect('internal:serviceRequest.upload', id)

        if len(myfile.name) >= 55:
            messages.error(
                request,
                'El nombre del archivo que intentó subir no debe exceder los 50 caracteres'
            )
            return redirect('internal:serviceRequest.upload', id)

        # fs = FileSystemStorage()
        description = request.POST.get('text_description')
        name = request.POST.get('text_name')

        if name:
            if validate_name(name):
                if ('.' in myfile.name):
                    nameWithExtension = name + myfile.name[myfile.name.rfind("."):]
                else:
                    nameWithExtension = name
                matches = RequestAttachment.all_objects.filter(
                    deleted__isnull=True, fileName=nameWithExtension)
                if not matches:
                    requestAttach = RequestAttachment.all_objects.create(
                        request=sr_object,
                        description=description,
                        fileName="default"
                    )
                    fs = requestAttach.file
                    filename = fs.save(nameWithExtension, myfile)
                    requestAttach.fileName = nameWithExtension
                    requestAttach.save()
                else:
                    messages.error(
                        request,
                        'El nombre del archivo que intentó subir ya existe'
                    )
                    return redirect('internal:serviceRequest.upload', id)
            else:
                messages.error(
                    request,
                    'El nombre del archivo que intentó subir no es válido.'
                )
                return redirect('internal:serviceRequest.upload', id)
        else:
            if ('.'in myfile.name):
                valido = validate_name(myfile.name[:myfile.name.rfind(".")])
            else:
                valido = validate_name(myfile.name)
            if (valido):
                matches = RequestAttachment.all_objects.filter(
                    deleted__isnull=True, fileName=myfile.name)
                if len(list(matches)) == 0:
                    requestAttach = RequestAttachment.all_objects.create(
                        request=sr_object,
                        description=description,
                        fileName="default"
                    )
                    fs = requestAttach.file
                    fs.save(myfile.name, myfile)
                    requestAttach.fileName = requestAttach.file.name.split('/')[-1]
                    requestAttach.save()
                else:
                    messages.error(
                        request,
                        'El nombre del archivo que intentó subir ya existe'
                    )
                    return redirect('internal:serviceRequest.upload', id)
            else:
                messages.error(
                    request,
                    'El nombre del archivo que intentó subir no es válido.'
                )
                return redirect('internal:serviceRequest.upload', id)
        messages.success(
            request,
            'Se ha subido el archivo "' +
            requestAttach.fileName +
            '" exitosamente!'
        )
        return redirect('internal:serviceRequest.attachmentList', id)

    context = {
        'servicerequest': sr_object,
    }
    return render(request, 'internal/serviceRequest/attachFile.html', context)


def attachmentList(request, id):
    sr_object = get_object_or_404(ServiceRequest, pk=id)
    requestAttachment_list = RequestAttachment.all_objects.filter(
        deleted__isnull=True,
        request=sr_object
    )

    context = {
        'serviceRequest': sr_object,
        'requestAttachment_list': requestAttachment_list,
    }
    template = 'internal/serviceRequest/files.html'
    return render(request, template, context)


def showAttachedFile(request, id):
    template = 'internal/serviceRequest/showAttachedFile.html'
    context = {
        'selected_file': RequestAttachment.all_objects.get(pk=id),
    }
    return render(request, template, context)


def editAttachedFile(request, id):
    if request.method == 'POST':
        fileAttach = RequestAttachment.all_objects.get(pk=id)
        description = request.POST.get('descripcionInput')
        name = request.POST.get('nombreArchivoInput')
        if not name:
            messages.error(request, 'No puede dejar el nombre vacío!')
            return redirect('internal:serviceRequest.editAttachedFile', id)
        nameWithExtension = name + \
            fileAttach.file.name[fileAttach.file.name.rfind("."):]
        if (fileAttach.fileName == nameWithExtension and
           fileAttach.description == description):
            return redirect(
                'internal:serviceRequest.attachmentList',
                fileAttach.request.pk
            )
        matches = RequestAttachment.all_objects.filter(
            deleted__isnull=True, fileName=nameWithExtension).exclude(pk=id)
        if not matches:
            fileAttach.fileName = nameWithExtension
            fileAttach.save()
        else:
            messages.error(request, 'Ya existe un archivo con ese nombre!')
            return redirect('internal:serviceRequest.editAttachedFile', id)
        fileAttach.description = description
        fileAttach.save()
        messages.success(
            request, 'Se han actualizado los datos del archivo exitosamente!')
        return redirect(
            'internal:serviceRequest.attachmentList',
            fileAttach.request.pk
        )
    template = 'internal/serviceRequest/editAttachedFile.html'
    context = {
        'selected_file': RequestAttachment.all_objects.get(pk=id),
    }
    return render(request, template, context)


def deleteAttachedFile(request, id):
    requestAttached = RequestAttachment.all_objects.get(pk=id)
    idRequest = requestAttached.request.pk
    filename = requestAttached.fileName
    requestAttached.file.delete()
    requestAttached.delete()
    messages.success(request, 'El archivo "' + filename +
                     '" se eliminó exitosamente!')
    return redirect('internal:serviceRequest.attachmentList', idRequest)


def downloadAttachedFile(request, id):
    requestAttachment = RequestAttachment.all_objects.get(pk=id)
    filename = requestAttachment.file.name.split('/')[-1]
    response = HttpResponse(requestAttachment.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response


def reportGenerator(request, id):
    template = 'internal/servicerequest/reportGeneratorView.html'
    serviceRequest = ServiceRequest.all_objects.get(pk=id)
    sample_list = Sample.all_objects.filter(
        deleted__isnull=True, request=serviceRequest)
    context = {
        'sample_list': sample_list,
        'servicerequest': serviceRequest,
    }
    return render(request, template, context)


def getEssayFillList(sample):
    essayFillQuerySet = EssayFill.all_objects.filter(
        deleted__isnull=True,
        sample=sample)  # Deberia ser solo 1 ensayo
    essayFillList = list(essayFillQuerySet)
    return essayFillList


def getParameterFillList(methodFill):
    ParameterQuerySet = EssayMethodParameterFill.all_objects.filter(
        deleted__isnull=True, essay_method=methodFill)
    ParameterFillList = list(ParameterQuerySet)
    return ParameterFillList


def getMethodFillList(essayFill):
    MethodsQuerySet = EssayMethodFill.all_objects.filter(
        deleted__isnull=True, essay=essayFill, chosen=True)
    MethodsList = list(MethodsQuerySet)
    return MethodsList


def reportDetail(request,
                 template='internal/servicerequest/reportDetail.html'):
    if request.POST:
        if "b_cancel" in request.POST:
            return redirect('internal:servicerequest.index')
        list_samples_id = request.POST.getlist('checks[]')
        if len(list_samples_id) > 0:
            SampleCompleteList = []
            EssayFillCompleteList = []
            MethodFillCompleteList = []
            ParameterFillCompleteList = []
            for samples_id in list_samples_id:
                sample = Sample.all_objects.get(pk=samples_id)
                SampleCompleteList.append(sample)
                essayFillList = getEssayFillList(sample)
                EssayFillCompleteList.append(essayFillList)
                thisSamplesMethodFillList = []
                thisSamplesParameterFillList = []
                for essayFill in essayFillList:
                    MethodFillList = getMethodFillList(essayFill)
                    thisSamplesMethodFillList.append(MethodFillList)
                    thisEssaysParameterFillList = []
                    for methodFill in MethodFillList:
                        ParameterFillList = getParameterFillList(methodFill)
                        thisEssaysParameterFillList.append(ParameterFillList)
                    thisSamplesParameterFillList.append(
                        thisEssaysParameterFillList)
                MethodFillCompleteList.append(thisSamplesMethodFillList)
                ParameterFillCompleteList.append(thisSamplesParameterFillList)

            context = {
                'SampleCompleteList': SampleCompleteList,
                'EssayFillCompleteList': EssayFillCompleteList,
                'MethodFillCompleteList': MethodFillCompleteList,
                'ParameterFillCompleteList': ParameterFillCompleteList,
            }
            pdf = render_to_pdf(
                'internal/servicerequest/reportDetailPDF.html', context)
            return HttpResponse(pdf, content_type='application/pdf')
            # return render(request, template, context)
        else:
            messages.error(
                request,
                'Debe seleccionar una muestra!'
            )
            return redirect(
                'internal:servicerequest.reportGenerator',
                request.POST.get("b_reporte")
            )
    else:
        return redirect('internal:servicerequest.index')


def finalReport(request,
                id,
                template='internal/servicerequest/reportDetail.html'):
    serviceRequest = ServiceRequest.all_objects.get(pk=id)
    list_samples_id = Sample.all_objects.filter(
        deleted__isnull=True, request=serviceRequest)
    if list_samples_id:
        SampleCompleteList = []
        EssayFillCompleteList = []
        MethodFillCompleteList = []
        ParameterFillCompleteList = []
        for samples in list_samples_id:
            sample = Sample.all_objects.get(pk=samples.pk)
            SampleCompleteList.append(sample)
            essayFillList = getEssayFillList(sample)
            EssayFillCompleteList.append(essayFillList)
            thisSamplesMethodFillList = []
            thisSamplesParameterFillList = []
            for essayFill in essayFillList:
                MethodFillList = getMethodFillList(essayFill)
                thisSamplesMethodFillList.append(MethodFillList)
                thisEssaysParameterFillList = []
                for methodFill in MethodFillList:
                    ParameterFillList = getParameterFillList(methodFill)
                    thisEssaysParameterFillList.append(ParameterFillList)
                thisSamplesParameterFillList.append(
                    thisEssaysParameterFillList)
            MethodFillCompleteList.append(thisSamplesMethodFillList)
            ParameterFillCompleteList.append(thisSamplesParameterFillList)

        context = {
            'SampleCompleteList': SampleCompleteList,
            'EssayFillCompleteList': EssayFillCompleteList,
            'MethodFillCompleteList': MethodFillCompleteList,
            'ParameterFillCompleteList': ParameterFillCompleteList,
        }
        pdf = render_to_pdf(
            'internal/servicerequest/finalReportPDF.html', context)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "InformeFinal-%s.pdf" % ("Nombre del cliente")
            filenameNoSpaces = "".join(filename.split())
            content = "inline; filename='%s'" % (filenameNoSpaces)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" % (filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse("Not found")
        # return HttpResponse(pdf, content_type='application/pdf')
        # return render(request, template, context)
    else:
        messages.error(
            request,
            'No puede generar un informe de una solicitud que no tiene muestras'
        )
        return redirect(reverse('internal:servicerequest.index'), id)


def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("utf-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None


def reportDetailPDF(request):
    return
