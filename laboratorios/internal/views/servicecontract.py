# class ServiceContract(models.Model):
#    client = models.ForeignKey(Client, on_delete=models.CASCADE)
#    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)


# class ServiceContractModification(models.Model):
#    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE)
#    description = models.CharField(max_length=100)


# Se va a realizar la vista de como un empleado realizaria la modificacion de un contrato a peticion del cliente.
# Luego se verá como hacer la vista propia del cliente

from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from internal.models import *


def index(request,
          template='internal/servicecontract/index.html',
          extra_context=None):
    contracts = ServiceContract.all_objects.filter(deleted__isnull=True)
    context = {
        'servicecontract_list': contracts,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         service_id,
         template='internal/servicecontract/show.html'):
    servicecontract = get_object_or_404(
        ServiceContract.all_objects,
        pk=service_id
    )
    client = get_object_or_404(
        Client.all_objects,
        pk=servicecontract.client.id
    )
    servicerequest = get_object_or_404(
        ServiceRequest.all_objects,
        pk=servicecontract.request.id
    )
    #search = servicerequest.id
    #selected_samples = Sample.objects.filter(request__id = search)     # Filtramos por el campo request.id de la clase Sample
    context = {
        'client': client,
        'servicerequest': servicerequest,
        #'selected_samples': selected_samples
    }
    return render(request, template, context)


def delete(request, pk):

    servicecontract = get_object_or_404(ServiceContract.all_objects, pk=pk)
    servicerequest = get_object_or_404(
        ServiceRequest.all_objects,
        pk=servicecontract.request.pk
    )
    servicecontract.delete()

    return redirect('internal:servicecontract.index')


def edit(request,
         pk, template='internal/servicerequest/index.html'):
    service_contract = ServiceContract.objects.get(pk=pk)
    request_id = service_contract.request.pk
    service_request = ServiceRequest.objects.get(pk=request_id)

    state = ServiceRequestState.objects.get(slug="modified")
    service_request.state = state  # Le asignamos el estado de "Modificado"
    service_request.save()

    service_contract.delete()       # Borramos el contrato

    return redirect("internal:servicerequest.edit", request_id)
    # return redirect(reverse("internal:servicecontract.index"))
    # return redirect(reverse_lazy("internal:servicerequest.index", request_id))


def approve(request,
            pk, template='internal/servicecontract/index.html'):

    return redirect(reverse("internal:servicecontract.index"))
