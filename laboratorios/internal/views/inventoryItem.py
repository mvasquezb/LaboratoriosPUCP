from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.contrib import messages
from internal.models import *
from internal.views.forms import (
    InventoryItemEditForm
)
from django.contrib.auth.decorators import user_passes_test
from internal.permissions.inventoryItem import *


def index(request,
          template='internal/inventoryItem/index.html',
          extra_context=None):
    inventoryItems = InventoryItem.objects.order_by('sample__name')

    context = {
        'inventoryItem_list': inventoryItems,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         pk,
         template='internal/inventoryItem/show.html'):
    inventoryItems = get_object_or_404(
        InventoryItem,
        pk=pk
    )
    context = {
        'inventoryItem': inventoryItems
    }
    return render(request, template, context)


@user_passes_test(delete_inventory_item_check, login_url='internal:index')
def delete(request, pk):
    inventoryItems = get_object_or_404(
        InventoryItem,
        pk=pk
    )
    inventoryItems.delete()

    return redirect('internal:inventoryItem.index')


@user_passes_test(edit_inventory_item_check, login_url='internal:index')
def edit(request, pk,
         template='internal/inventoryItem/edit.html'):


    inventoryItems = get_object_or_404(
        InventoryItem,
        pk=pk
    )
    form = InventoryItemEditForm(request.POST or None, instance=inventoryItems)

    context = {
        'inventoryItem': inventoryItems,
    }

    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Se ha editado con exito')
            return redirect('internal:inventoryItem.index')
        else:
            messages.warning(request, 'Datos invalidos')
    return render(request, template, context)

