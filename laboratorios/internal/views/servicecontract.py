from django.shortcuts import (
    render,
    get_object_or_404,
    get_list_or_404,
    redirect,
    reverse,
)
from ..models import *
from ..views.forms import *


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
         pk,
         template='internal/servicecontract/edit.html'):

    service_contract = get_object_or_404(
        ServiceContract,
        pk=pk
    )
    request_id_mod = service_contract.request.pk
    service_request_mod = get_object_or_404(
        ServiceRequest.all_objects,
        pk=request_id_mod
    )

    state = get_object_or_404(
        ServiceRequestState.all_objects.filter(deleted__isnull=True),
        description="Modificado"
    )

    service_request_mod.state = state  # Le asignamos el estado de "Modificado"
    service_request_mod.save()

    # Creamos el original, pero aun no lo guardamos
    service_request_ori = ServiceRequest.objects.get(pk=request_id_mod)
    service_request_ori.pk = None

    #####################################################################
    service_request_form = ServiceRequestForm(
        request.POST or None, instance=service_request_mod)
    # For all samples and their selected essayFills in list
    sample_list = Sample.all_objects.filter(
        deleted__isnull=True,
        request=service_request_mod
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
        'service_request': service_request_mod,
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
        service_request_form.save()  # Guarda los cambios de la modificacion

        # Ya fue verificado así que podemos comenzar a guardar

        # Copiamos el priority, pues en el edit no se establece ello
        if service_request_ori.priority is not None:
            service_request_mod.priority = get_object_or_404(
                ServiceRequestPriority.all_objects,
                pk=service_request_ori.priority.pk
            )
            service_request_mod.save()

        service_request_ori.save()      # Guardamos el original
        service_contract_modification = ServiceContractModification(
            contract=service_contract,
            description=service_request_ori.pk
        )

        service_contract_modification.save()

        # add save for each form
        for i in range(0, len(essay_methods_chosen_forms)):
            for j in range(0, len(essay_methods_chosen_forms[i])):
                print(essay_methods_chosen_forms[i][j].save().chosen)
                essay_methods_chosen_forms[i][j].save()
        return redirect(reverse("internal:servicecontract.index"))
    return render(request, template, context)


def approve(request,
            pk, template='internal/servicecontract/index.html'):
    # obtenemos todos las modificaciones que no han sido eliminados
    all_contract_mods = ServiceContractModification.all_objects.filter(
        deleted__isnull=True
    )
    # obtenemos el contrato modificado
    service_contract_mod = get_list_or_404(
        all_contract_mods,
        contract=pk
    )

    idrequestMod = service_contract_mod[0].contract.request.pk
    # Obtenemos el id del servicio original asociado al contrato
    idrequestOri = int(service_contract_mod[0].description)

    service_request_Mod = get_object_or_404(
        ServiceRequest.all_objects, pk=idrequestMod)
    service_request_Ori = get_object_or_404(
        ServiceRequest.all_objects, pk=idrequestOri)

    # Se va a aprobar la modificacion por lo cual, el estado de dicho servicio
    # será aprobado y el otro será borrado
    state = get_object_or_404(
        ServiceRequestState.all_objects.filter(deleted__isnull=True),
        description="Aprobado"
    )
    service_request_Mod.state = state  # Le asignamos el estado de "Aprobado"
    service_request_Mod.save()
    service_request_Ori.delete()              # Borramos el servicio original

    # Borramos el registro de modificacion de contrato
    service_contract_mod[0].delete()
    # El modificado ya estaba asociado al contrato asi que no habrá más cambios

    return redirect("internal:servicecontract.index")


def refuse(request,
           pk, template='internal/servicecontract/index.html'):
    all_contract_mods = ServiceContractModification.all_objects.filter(
        deleted__isnull=True)  # obtenemos todos las modificaciones que no han sido eliminados
    service_contract_mod = get_list_or_404(
        all_contract_mods, contract=pk)  # obtenemos el contrato modificado

    idrequestMod = service_contract_mod[0].contract.request.pk
    # Obtenemos el id del servicio original asociado al contrato
    idrequestOri = int(service_contract_mod[0].description)

    service_request_Mod = get_object_or_404(
        ServiceRequest.all_objects, pk=idrequestMod)
    service_request_Ori = get_object_or_404(
        ServiceRequest.all_objects, pk=idrequestOri)

    # Se va a rechazar la modificacion por lo cual, pasaremos todos los datos
    # del original al modificado

    state = get_object_or_404(
        ServiceRequestState.all_objects.filter(deleted__isnull=True),
        description="Aprobado"
    )

    service_request_Ori.state = state  # Le asignamos el estado de "Aprobado"
    service_request_Mod.client = Client.objects.get(
        pk=service_request_Ori.client.pk)
    service_request_Mod.supervisor = Employee.objects.get(
        pk=service_request_Ori.supervisor.pk)
    service_request_Mod.priority = ServiceRequestPriority.objects.get(
        pk=service_request_Ori.priority.pk)
    service_request_Mod.state = get_object_or_404(
        ServiceRequestState.all_objects, pk=service_request_Ori.state.pk)
    if service_request_Ori.external_provider != None:
        service_request_Mod.external_provider = get_object_or_404(ExternalProvider.all_objects,
                                                                  pk=service_request_Ori.external_provider.pk)

    service_request_Mod.observations = service_request_Ori.observations                 # cadena
    service_request_Mod.expected_duration = service_request_Ori.expected_duration       # integer

    service_request_Mod.save()      # Guardamos los cambios

    service_request_Ori.delete()
    # Borramos el registro de modificacion de contrato
    service_contract_mod[0].delete()

    return redirect("internal:servicecontract.index")
