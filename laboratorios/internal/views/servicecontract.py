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
    get_list_or_404,
    redirect,
    reverse,
)
from django.contrib import messages
from ..models import *


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
    request_id = service_contract.request.pk
    service_request = get_object_or_404(ServiceRequest.all_objects, pk=request_id)

    state = get_object_or_404(ServiceRequestState.all_objects, description ="Modificado")

    service_request.state = state  # Le asignamos el estado de "Modificado"
    service_request.save()

    # Creamos un ServiceRequest de copia, el cual almacenará la modificación
    service_request_mod = ServiceRequest(client = service_request.client, supervisor = service_request.supervisor,
                                         priority = service_request.priority, state = service_request.state,
                                         external_provider = service_request.external_provider, observations = service_request.observations,
                                         expected_duration = service_request.expected_duration)
    service_request_mod.save()

    # Asociamos el servicio modificado al contrato
    service_contract.request = service_request_mod
    service_contract.save()

    # Creamos el ServiceContractModification
    service_contract_modification = ServiceContractModification(contract = service_contract, description = request_id)
    service_contract_modification.save()

    return redirect("internal:servicerequest.edit", service_request_mod.pk)



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

############################################################
def refuse (request,
            pk, template='internal/servicecontract/index.html'):
    service_contracts_mod_total = ServiceContractModification.all_objects.filter(deleted__isnull=True)  # obtenemos todos las modificaciones que no han sido eliminados
    service_contract_mod = get_list_or_404(service_contracts_mod_total, contract=pk)  # obtenemos el contrato modificado

    idrequestMod = service_contract_mod[0].contract.request.pk
    idrequestOri = int(service_contract_mod[0].description)    # Obtenemos el id del servicio original asociado al contrato

    service_request_Mod = get_object_or_404(ServiceRequest.all_objects, pk=idrequestMod)
    service_request_Ori = get_object_or_404(ServiceRequest.all_objects, pk=idrequestOri)

    # Se va a rechazar la modificacion por lo cual, el estado del servicio original será aprobado y el otro será borrado
    state = get_object_or_404(ServiceRequestState.all_objects, description="Aprobado")
    service_request_Ori.state = state  # Le asignamos el estado de "Aprobado"
    service_request_Ori.save()
    service_request_Mod.delete              # Borramos el servicio modificado
    # El original no estaba asociado al contrato asi que habrá que hacerlo
    service_contract_mod[0].contract.request = service_request_Ori
    service_contract_mod[0].delete         #####################################3

    return redirect("internal:servicecontract.index")
