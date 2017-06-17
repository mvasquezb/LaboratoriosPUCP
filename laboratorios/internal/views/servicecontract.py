# class ServiceContract(models.Model):
#    client = models.ForeignKey(Client, on_delete=models.CASCADE)
#    request = models.ForeignKey(ServiceRequest, on_delete=models.CASCADE)


# class ServiceContractModification(models.Model):
#    contract = models.ForeignKey(ServiceContract, on_delete=models.CASCADE)
#    description = models.CharField(max_length=100)


# Se va a realizar la vista de como un empleado realizaria la modificacion de un contrato a peticion del cliente.
# Luego se verá como hacer la vista propia del cliente

import copy

from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from ..models import *
from ..views.forms import ClientForm, EmployeeForm
from django.core.urlresolvers import reverse_lazy


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

    context = {
        'client': client,
        'servicerequest': servicerequest,
    }
    return render(request, template, context)


def delete(request, pk):
    servicecontract = get_object_or_404(ServiceContract.all_objects, pk=pk)
    servicerequest = get_object_or_404(
        ServiceRequest.all_objects,
        pk=servicecontract.request.pk
    )

    servicerequest.delete()
    servicecontract.delete()

    return redirect('internal:servicecontract.index')


def edit(request,
         pk, template='internal/servicerequest/edit.html'):

    service_contract = get_object_or_404(ServiceContract.all_objects, pk=pk)
    request_id_mod = service_contract.request.pk
    service_request_mod = get_object_or_404(ServiceRequest.all_objects, pk=request_id_mod)

    state = get_object_or_404(ServiceRequestState.all_objects, description ="Modificado")

    service_request_mod.state = state  # Le asignamos el estado de "Modificado"
    service_request_mod.save()

    # Creamos un ServiceRequest de copia, el cual almacenará el original
    service_request_ori = ServiceRequest(client = service_request_mod.client,
                                         supervisor = service_request_mod.supervisor,
                                         priority = service_request_mod.priority,
                                         state = service_request_mod.state,
                                         external_provider = service_request_mod.external_provider,
                                         observations = service_request_mod.observations,
                                         expected_duration = service_request_mod.expected_duration)
    service_request_ori.save()

    # Entonces, el modificado ya estará asociado al contrato

    # Creamos el ServiceContractModification
    service_contract_modification = ServiceContractModification(contract = service_contract, description = service_request_ori.pk)
    service_contract_modification.save()

    return redirect("internal:servicerequest.edit", request_id_mod)



def approve(request,
            pk, template='internal/servicecontract/index.html'):

    service_contracts_mod_total = ServiceContractModification.all_objects.filter(deleted__isnull=True)        # obtenemos todos las modificaciones que no han sido eliminados
    service_contract_mod = get_list_or_404(service_contracts_mod_total, contract=pk)            # obtenemos el contrato modificado

    idrequestMod = service_contract_mod[0].contract.request.pk
    idrequestOri = int(service_contract_mod[0].description)    # Obtenemos el id del servicio original asociado al contrato

    service_request_Mod = get_object_or_404(ServiceRequest.all_objects, pk=idrequestMod)
    service_request_Ori = get_object_or_404(ServiceRequest.all_objects, pk=idrequestOri)

    # Se va a aprobar la modificacion por lo cual, el estado de dicho servicio será aprobado y el otro será borrado
    state = get_object_or_404(ServiceRequestState.all_objects, description="Aprobado")
    service_request_Mod.state = state  # Le asignamos el estado de "Aprobado"
    service_request_Mod.save()
    service_request_Ori.delete              # Borramos el servicio original
    # El modificado ya estaba asociado al contrato asi que no habrá más cambios

    return redirect("internal:servicecontract.index")


def refuse (request,
            pk, template='internal/servicecontract/index.html'):
    service_contracts_mod_total = ServiceContractModification.all_objects.filter(deleted__isnull=True)  # obtenemos todos las modificaciones que no han sido eliminados
    service_contract_mod = get_list_or_404(service_contracts_mod_total, contract=pk)  # obtenemos el contrato modificado

    idrequestMod = service_contract_mod[0].contract.request.pk
    idrequestOri = int(service_contract_mod[0].description)    # Obtenemos el id del servicio original asociado al contrato

    service_request_Mod = get_object_or_404(ServiceRequest.all_objects, pk=idrequestMod)
    service_request_Ori = get_object_or_404(ServiceRequest.all_objects, pk=idrequestOri)

    # Se va a rechazar la modificacion por lo cual, pasaremos todos los datos del original al modificado
    state = get_object_or_404(ServiceRequestState.all_objects, description="Aprobado")
    service_request_Ori.state = state  # Le asignamos el estado de "Aprobado"

    service_request_Mod.client = service_request_Ori.client
    service_request_Mod.supervisor = service_request_Ori.supervisor
    service_request_Mod.priority = service_request_Ori.priority
    service_request_Mod.state = service_request_Ori.state
    service_request_Mod.external_provider = service_request_Ori.external_provider
    service_request_Mod.observations = service_request_Ori.observations
    service_request_Mod.expected_duration = service_request_Ori.expected.duration

    service_request_Mod.save()

    service_request_Ori.delete()

    return redirect("internal:servicecontract.index")
