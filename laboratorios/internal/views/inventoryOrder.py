from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from ..models import *

def index(request,
          template='internal/inventoryOrder/index.html',
          extra_context=None):
    #types = InventoryOrder.objects.all()
    #context = {'inventoryOrder_list': types}

    search = request.GET.get('search')
    if search:
       inventoryOrder_listAux = InventoryOrder.objects.filter(
       essay__sample__name__icontains=search,
        #).order_by('username')
       ).order_by('essay__sample__name')
       inventoryOrder_list = inventoryOrder_listAux.objects.filter(unsettled = True)
    else:
        inventoryOrder_list = InventoryOrder.objects.filter(unsettled = True).order_by('essay__sample__name')


    #inventoryOrder_list = InventoryOrder.objects.all()

    paginator = Paginator(inventoryOrder_list, 3)
    page = request.GET.get('page')
    try:
        inventoryOrder = paginator.page(page)
    except PageNotAnInteger:
        inventoryOrder = paginator.page(1)
    except EmptyPage:
        inventoryOrder = paginator.page(paginator.num_pages)

    context = {
        'inventoryOrder_list': inventoryOrder,
        'paginator': paginator,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

    #return render(request, template, context)

def show(request,
         pk,
         template='internal/inventoryOrder/show.html'):
    inventoryOrder = get_object_or_404(InventoryOrder, pk=pk)
    context = {
        'inventoryOrder': inventoryOrder
    }
    return render(request, template, context)

#def index(request,
#          template='internal/inventoryOrder/index.html',
#          extra_context=None):
#    search = request.GET.get('search')
#    if search:
#        inventoryOrder_list = InventoryOrder.objects.filter(
#            username__icontains=search
#        ).order_by('essay.essay.name')
#    else:
#        inventoryOrder_list = InventoryOrder.objects.order_by('essay.essay.name')
#
#    paginator = Paginator(inventoryOrder_list, 3)
#    page = request.GET.get('page')
#    try:
#        inventoryOrder = paginator.page(page)
#    except PageNotAnInteger:
#        inventoryOrder = paginator.page(1)
#    except EmptyPage:
#        inventoryOrder = paginator.page(paginator.num_pages)
#
#    context = {
#        'inventoryOrder_list': inventoryOrder,
#        'paginator': paginator,
#    }
#    if extra_context is not None:
#        context.update(extra_context)
#    return render(request, template, context)

def aprobar(request, pk):
    inventoryOrder = get_object_or_404(InventoryOrder, pk=pk)
    inventoryOrder.unsettled = False
    #Falta crear añadir inventory item
    #stored = InventoryItem.__new__()

    #newInventoryItem = InventoryItem( sample = inventoryOrder.essay.sample , quantity = inventoryOrder.essay.quantity)
    newInventoryItem = InventoryItem(sample = inventoryOrder.essay.sample, quantity=inventoryOrder.essay.quantity)
    #newInventoryItem = InventoryItem( inventoryOrder.essay.sample._get_pk_val , inventoryOrder.essay.quantity)

    newInventoryItem.save()
    inventoryOrder.save()
    messages.success(request, 'Se almaceno la muestra con exito!')
    return redirect('internal:inventoryOrder.index')

#def create(request,
#           template='internal/employee/create.html'):
#    form = EmployeeForm(request.POST or None)
#    context = {
#        'laboratories': Laboratory.objects.all(),
#        'roles': Role.objects.all(),
#        'form': form
#    }
#    if request.method == 'POST':
#        if form.is_valid():
#            form.save()
#            messages.success(request, 'Se ha creado el empleado exitosamante!')
#            return redirect('internal:employee.index')
#    return render(request, template, context)


def rechazar(request, pk):
    inventoryOrder = get_object_or_404(InventoryOrder, pk=pk)
    inventoryOrder.unsettled = False
    inventoryOrder.save()
    messages.success(request, 'Se rechazo el almacenamiento con exito!')
    #messages.success(request, 'Se rechazo el almacenamiento!')
    return redirect('internal:inventoryOrder.index')

#def aprobar(request,
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
    #    types = InventoryOrder.objects.all()
    #    context = {'inventoryOrder_list': types}
#    return render(request, template, context)
    #return redirect('requestStorage.index')

#def rechazar(request,
    #          template='internal/inventoryOrder/index.html',
    #          extra_context=None):
    #    if request.method == 'GET':
    #        x = dict(request.GET)
#        for i in x['array[]']:
#            old = InventoryOrder.objects.get(pk=i)
            #            old.pendiente = False
            #            old.aprobado = False
            #            old.save()

            #    types = InventoryOrder.objects.all()
#    context = {'inventoryOrder_list': types}
#    return render(request, template, context)
