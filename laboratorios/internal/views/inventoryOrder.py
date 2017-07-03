from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from internal.models import *
from internal.views.forms import (
    InventoryOrderForm,
    InventoryOrderEditForm
)
from internal.permissions import user_passes_test
from internal.permissions.inventoryOrder import *


@user_passes_test(index_inventory_order_check, login_url='internal:index')
def index(request,
          template='internal/inventoryOrder/index.html',
          extra_context=None):
    #inventoryOrders = InventoryOrder.all_objects.order_by('essay__sample__name')
    inventoryOrders = InventoryOrder.all_objects.filter(
        deleted__isnull=True,
        unsettled=True
    ).order_by('essay__sample__name')

    context = {
        'inventoryOrder_list': inventoryOrders,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(show_inventory_order_check, login_url='internal:index')
def show(request,
         pk,
         template='internal/inventoryOrder/show.html'):
    inventoryOrder = get_object_or_404(
        InventoryOrder.all_objects.filter(deleted__isnull=True),
        pk=pk
    )
    context = {
        'inventoryOrder': inventoryOrder
    }
    return render(request, template, context)


def check(request,
          template='internal/inventoryOrder/indexCheck.html',
          extra_context=None):
    inventoryOrder_listF = InventoryOrder.objects.filter(
        deleted__isnull=True,
        unsettled=True
    ).order_by('essay__sample__name')

    # inventoryOrder_list = InventoryOrder..objects.filter(deleted__isnull=True)
    context = {
        'inventoryOrder_list': inventoryOrder_listF,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


@user_passes_test(create_inventory_order_check, login_url='internal:index')
def create(request,
           template='internal/inventoryOrder/create.html'):
    form = InventoryOrderForm(request.POST or None)
    #Solo puedo crear solicitud de muestras en solicitudes en estado espera de muestras
    #esta revisando muestras
    context = {
        'essayies': EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample__request__state__slug = 'wait_for_samples') | EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample__request__state__slug = 'review_samples'
        ),

    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha creado la solicitud exitosamante!')
            return redirect('internal:inventoryOrder.index')
    return render(request, template, context)

def createPK(request,
           pk,
           template='internal/inventoryOrder/createPK.html'):
    actualInventoryOrder = get_object_or_404(
        EssayFill.all_objects.filter(deleted__isnull=True),
        pk=pk
    )
    form = InventoryOrderForm(request.POST or None)
    # Solo puedo crear solicitud de muestras en solicitudes en estado espera de muestras
    # o esta revisando muestras
    context = {
        'essayies': EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample__request__state__slug = 'wait_for_samples') | EssayFill.all_objects.filter(
            deleted__isnull=True,
            sample__request__state__slug = 'review_samples'
        ),
        'actualInventoryOrder': actualInventoryOrder,
    }
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha creado la solicitud exitosamante!')
            return redirect('internal:inventoryOrder.index')
    return render(request, template, context)


@user_passes_test(edit_inventory_order_check, login_url='internal:index')
def edit(request, pk1, pk,
         template='internal/inventoryOrder/edit.html'):
    inventoryOrder = get_object_or_404(
        InventoryOrder.all_objects.filter(deleted__isnull=True),
        pk=pk1
    )
    newinventoryOrder = get_object_or_404(
        EssayFill.all_objects.filter(deleted__isnull=True),
        pk=pk
    )
    form = InventoryOrderEditForm(request.POST or None, instance=inventoryOrder)
    context = {
        'inventoryOrder': inventoryOrder,
        'newinventoryOrder': newinventoryOrder,
        'essayies': EssayFill.all_objects.filter(deleted__isnull=True),
    }

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha editado con exito')
            return redirect('internal:inventoryOrder.index')
        else:
            messages.warning(request, 'Datos invalidos')
    return render(request, template, context)


def approve(request, pk, pk2):
    inventoryOrder = get_object_or_404(
        InventoryOrder.all_objects.filter(deleted__isnull=True),
        pk=pk
    )

    inventoryOrder.unsettled = False
    # Creo inventory Item
    newInventoryItem = InventoryItem(
        sample=inventoryOrder.essay.sample,
        quantity=inventoryOrder.essay.quantity
    )
    newInventoryItem.save()

    #Busco el estado de revisando muestras
    newState = get_object_or_404(
        ServiceRequestState.all_objects.filter(deleted__isnull=True,
            slug='review_samples'),
    )

    #Modifico el estado del la solicitud
    changeRequest = get_object_or_404(
        ServiceRequest.all_objects.filter(deleted__isnull=True),
        pk=pk2
    )
    changeRequest.state = newState

    #Guardo los cambios
    changeRequest.save()
    inventoryOrder.save()

    messages.success(request, 'Se almaceno la muestra con exito!')
    return redirect('internal:inventoryOrder.index')


def reject(request, pk):
    inventoryOrder = get_object_or_404(
        InventoryOrder.all_objects.filter(deleted__isnull=True),
        pk=pk
    )
    inventoryOrder.unsettled = False
    inventoryOrder.save()
    messages.success(request, 'Se rechazo el almacenamiento con exito!')
    return redirect('internal:inventoryOrder.index')


@user_passes_test(delete_inventory_order_check, login_url='internal:index')
def delete(request, pk):
    inventoryOrder = get_object_or_404(
        InventoryOrder.all_objects.filter(deleted__isnull=True),
        pk=pk
    )
    inventoryOrder.delete()

    return redirect('internal:inventoryOrder.index')


# def approve(request,
#          template='internal/inventoryOrder/index.html',
#          extra_context=None):
#    print(request.GET)
#    if request.method == 'GET' and 'array[]' in request.GET:
#        print("flag2")
    #        x = dict(request.GET)
    #        for i in x['array[]']:
    #            old = InventoryOrder.objects.get(pk=i)
    #            old.pendiente = False
    #            old.aprobado = True
    #            old.save()
    #    print("flag3")
    #    types = InventoryOrder.all_objects.filter(deleted__isnull=True)
    #    context = {'inventoryOrder_list': types}
#    return render(request, template, context)
    # return redirect('requestStorage.index')

# def reject(request,
    #          template='internal/inventoryOrder/index.html',
    #          extra_context=None):
    #    if request.method == 'GET':
    #        x = dict(request.GET)
#        for i in x['array[]']:
#            old = InventoryOrder.objects.get(pk=i)
    #            old.pendiente = False
    #            old.aprobado = False
    #            old.save()

    #    types = InventoryOrder.all_objects.filter(deleted__isnull=True)
#    context = {'inventoryOrder_list': types}
#    return render(request, template, context)
