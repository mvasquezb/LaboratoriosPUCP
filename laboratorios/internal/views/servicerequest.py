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
import json as simplejson
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


def index(request):
    context = {
        'requests': ServiceRequest.objects.all()
    }
    return render(request, 'internal/servicerequest/index.html', context)


def create(request,
           pk,
           template='internal/servicerequest/create.html'):
    selected_client = Client.objects.get(pk=pk)
    service_request_form = ServiceRequestForm(
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
            created_service_request = service_request_form.save()
            messages.success(
                request,
                'Se ha creado la solicitud exitosamante!'
            )
            return redirect(reverse('internal:servicerequest.index'))
    return render(request, template, context)


def select_client(request,
                  template='internal/servicerequest/select_client.html'):
    types = Client.objects.all().order_by('doc_number', 'username')
    context = {'client_list': types}
    return render(request, template, context)


def create_client(request,
                  template='internal/servicerequest/create_client.html'):
    form = ClientForm(request.POST or None)
    context = {'form': form}
    if form.is_valid():
        new_client = form.save()
        return redirect('internal:servicerequest.create', new_client.pk)
    return render(request, template, context)


def edit(request,
         pk,
         template='internal/servicerequest/edit.html'):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request_form = ServiceRequestForm(
        request.POST or None, instance=service_request)
    # For all samples and their selected essayFills in list
    sample_list = Sample.objects.filter(request=service_request)
    essay_fill_list = []
    essay_methods_list = []  # To get all essay_methods for every sample
    essay_methods_chosen_forms = []  # To get whether each essay_method is chosen or not

    for i in range(0, len(sample_list)):
        sample_listed = sample_list[i]
        essay_fill = EssayFill.objects.filter(
            sample=sample_listed
        ).first()

        essay_fill_list.append(essay_fill)
        essay_methods_list.append(
            EssayMethodFill.objects.filter(essay=essay_fill)
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
        'samples': sample_list,
        'essays': essay_fill_list,
        'essays_methods': essay_methods_list,
        'essay_methods_chosen_forms': essay_methods_chosen_forms,
        'pk': pk
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
    service_request = ServiceRequest.objects.get(pk=pk)
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
    sample = Sample.objects.get(pk=pk_sample)
    sample_form = SampleEditForm(request.POST or None, instance=sample)
    essay_fill_form = EssayFillSelectionForm(
        request.POST or None, instance=EssayFill.objects.get(sample=sample))
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


def delete(request,
           pk):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request.delete()
    return redirect(reverse("internal:servicerequest.index"))


def delete_sample(request,
                  pk_request,
                  pk_sample):
    sample = Sample.objects.get(pk=pk_sample)
    sample.delete()
    return redirect('internal:servicerequest.edit', pk_request)


def show(request, request_id):
    return edit(request, request_id)


def quotation(request,
              request_id,
              template='internal/servicerequest/quotation.html',
              extra_context=None):
    service_request = get_object_or_404(ServiceRequest, pk=request_id)
    quotation, created = Quotation.objects.get_or_create(
        request=service_request
    )
    essay_list = EssayFill.objects.filter(
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
    service_request = get_object_or_404(ServiceRequest, pk=request_id)
    sample = get_object_or_404(service_request.sample_set.all(), pk=sample_id)

    essay = sample.essayfill_set.first()
    essay_method_list = EssayMethodFill.objects.filter(
        essay=essay,
        chosen=True,
    ).distinct()

    employee_q = Q()
    for essay_method in essay_method_list:
        employee_q &= Q(essay_methods=essay_method.essay_method)
    employee_list = Employee.objects.filter(employee_q)
    form = ServiceAssignEmployeeForm(
        request.POST or None,
        employee=employee_list
    )

    query = Q()
    for essay_method in essay_method_list:
        query &= Q(assigned_essay_methods=essay_method)

    if employee_q:
        assigned_employee = employee_list.filter(query).first()
    else:
        assigned_employee = None

    # Está cagada esta lógica
    if request.method == 'POST':
        if form.is_valid():
            # Remove previous assigned employee, if existant
            employee = form.cleaned_data['employee']
            if assigned_employee and not employee == assigned_employee:
                assigned_employee.assigned_essay_methods.remove(
                    *essay_method_list
                )
            employee_methods = employee.assigned_essay_methods.all()
            methods_to_add = set(essay_method_list) - set(employee_methods)
            employee.assigned_essay_methods.add(*methods_to_add)

            if request.is_ajax():
                return JsonResponse({
                    'success': True,
                    'message': 'Se asignó la muestra correctamente',
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
        service_request = ServiceRequest.objects.get(pk=pk)
        state = ServiceRequestState.objects.get(description="Verificado")
        service_request.state = state  # Le asignamos el estado de aprobado
        service_request.save()
        client = Client.objects.get(pk=service_request.client.id)

        service_contract = ServiceContract(client=client, request=service_request)
        service_contract.save()  # Guardamos el service_contract en la tabla "ServiceContract"
        return redirect(reverse("internal:servicerequest.index"))


def workload_view_per_request(request,
    template='internal/servicerequest/workload_view_per_request.html'):
    month_names=['Enero','Febrero','Marzo','Abril','Mayo','Junio','Julio','Agosto','Septiembre','Octubre','Noviembre','Diciembre']
    service_request_list=ServiceRequest.objects.all()
    my_data=[]
    for i in range(0,len(service_request_list)):
        date_in_service = service_request_list[i].registered_date
        #date_in_service.strftime("%d/%m/%Y")
        #date_in_service.replace(day=date_in_service.day+service_request_list[i].expected_duration).strftime("%d/%m/%Y")

        # progresion calculation
        now = timezone.localtime(timezone.now())
        delta = now - date_in_service
        total = int(100*delta.days/service_request_list[i].expected_duration)


        my_dict={
        "id": service_request_list[i].id,
        "title": "Cliente" + service_request_list[i].client.get_full_name(),
        "start_date": date_in_service.strftime("%m/%d/%Y"), 
        "end_date": date_in_service.replace(day=date_in_service.day+service_request_list[i].expected_duration).strftime("%m/%d/%Y"),
        "value": 67,
        "term": "Short Term",
        "completion_percentage": total,
        "color": "#770051",
        }
        my_data.append(my_dict)
    js_data = simplejson.dumps(my_data)
    return render(request, template, {'js_data':js_data,'actual_month':month_names[now.month-1] + " " + str(now.year)})


def upload(request,id):
    if ("b_cancel" in request.POST):
        return redirect('internal:serviceRequest.attachmentList', id)

    if ("b_upload" in request.POST):
        if (len(request.FILES) != 0):
            if request.method == 'POST' and request.FILES['myfile']:
                myfile = request.FILES['myfile']
                if len(myfile.name) < 55:
                    #fs = FileSystemStorage()
                    sr_object = ServiceRequest.objects.get(pk=id)
                    description = str(request.POST.get('text_description'))
                    requestAttach= RequestAttachment.objects.create(request =sr_object,description = description,fileName="default")
                    fs = requestAttach.file
                    filename = fs.save(myfile.name, myfile)
                    requestAttach.fileName = requestAttach.file.name.split('/')[-1]
                    requestAttach.save()
                    messages.success(request, 'Se ha subido el archivo '+'"'+ requestAttach.fileName + '"' + ' exitosamente!')
                    return redirect('internal:serviceRequest.attachmentList', id)
                else:
                    messages.error(request,'El nombre del archivo que intentó subir no debe exceder los 50 caracteres!')
                    return redirect('internal:serviceRequest.upload', id)
        else:
            messages.error(request, 'Debe seleccionar un archivo!')
            return redirect('internal:serviceRequest.upload', id)
    else:
        return render(request, 'internal/serviceRequest/attachFile.html')
    #else:
    #    ra = RequestAttachment.objects.get(description = 'baka5')
    #    filename = ra.file.name.split('/')[-1]
    #    response = HttpResponse(ra.file, content_type='text/plain')
    #    response['Content-Disposition'] = 'attachment; filename=%s' % filename

     #   return response
 #       return render(request, 'internal/serviceRequest/attachFile.html')

 #   return redirect('internal:serviceRequest.attachmentList',id)
    #return render(request, 'internal/serviceRequest/attachFile.html')

def attachmentList(request,id):
    search = request.GET.get('search')
    sr_object = ServiceRequest.objects.get(pk=id)
    if search:
        requestAttachment_list = RequestAttachment.objects.filter(
            request=sr_object, fileName__icontains = search)
    else:
        requestAttachment_list = RequestAttachment.objects.filter(
            request=sr_object)

    paginator = Paginator(requestAttachment_list, 3)
    pageNumber = request.GET.get('page')
    try:
        requestAttachmentPageCurrent = paginator.page(pageNumber)
    except PageNotAnInteger:
        requestAttachmentPageCurrent = paginator.page(1)
    except EmptyPage:
        requestAttachmentPageCurrent = paginator.page(paginator.num_pages)

    context = {'serviceRequest': sr_object,
        'requestAttachment_list': requestAttachmentPageCurrent,
        'paginator': paginator,
    }
    template = 'internal/serviceRequest/files.html'
    return render(request, template, context)

def showAttachedFile(request,id):
    template = 'internal/serviceRequest/showAttachedFile.html'
    context = {
        'selected_file': RequestAttachment.objects.get(pk=id),
    }
    return render(request, template, context)

def deleteAttachedFile(request,id):
    requestAttached = RequestAttachment.objects.get(pk=id)
    idRequest = requestAttached.request.pk
    filename = requestAttached.fileName;
    requestAttached.file.delete()
    requestAttached.delete()
    messages.success(request, 'El archivo ' + '"' + filename + '"' +' se eliminó exitosamente!')
    return redirect('internal:serviceRequest.attachmentList',idRequest)

def downloadAttachedFile(request,id):
    requestAttachment = RequestAttachment.objects.get(pk=id)
    filename = requestAttachment.file.name.split('/')[-1]
    response = HttpResponse(requestAttachment.file, content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=%s' % filename

    return response

