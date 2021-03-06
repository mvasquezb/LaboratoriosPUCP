from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
)
from django.http import HttpResponse
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q, Count

from internal.models import *
from .forms import InventoryForm
import json as simplejson


def index(request,
          template='internal/inventory/index.html',
          extra_context=None):
    inventorys = Inventory.all_objects.all()
    context = {
        'inventorys_list': inventorys
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def manage_content(request,
                   pk):
    template = 'internal/inventory/manage_inventory_content.html'
    inventory = Inventory.all_objects.get(pk=pk)
    matches = ArticleInventory.all_objects.filter(
        inventory=inventory, deleted__isnull=True)
    inventory_types = Inventory.TYPE_CHOICES
    # Insumos
    if (inventory.get_inventory_type_display() == inventory_types[0][1]):
        articles = Supply.all_objects.filter(deleted__isnull=True)
    else:  # Equipos
        articles = Equipment.all_objects.filter(deleted__isnull=True)
    context = {
        'inventory': inventory,
        'inventory_types': inventory_types,
        'articles': articles,
        'matches': matches
    }
    return render(request, template, context)


def create(request,
           template='internal/inventory/create.html',
           extra_content=None):
    form = InventoryForm(request.POST or None)
    suplies = Supply.all_objects.filter(deleted__isnull=True)
    equipments = Equipment.all_objects.filter(deleted__isnull=True)
    if request.method == 'POST':
        if form.is_valid():
            print("FLAG1")
            form.save()
            messages.success(
                request, 'Se ha creado un nuevo inventario exitosamante!')
            return redirect('internal:inventory.index')
        else:
            for field in form:
                if field.errors:
                    if field.name == 'name':
                        messages.error(
                            request,
                            'Ya existe un inventario con este nombre'
                        )
                    else:
                        msg = field.label + ': ' + str(field.errors)
                        messages.error(request, msg)

    inventories = Inventory.all_objects.filter(deleted__isnull=True)
    inventory_types = Inventory.TYPE_CHOICES
    types = []
    for type_aux in inventory_types:
        types.append(type_aux[1])
    context = {
        'inventories': inventories,
        'form': form,
        'inventory_types': inventory_types,
        'supply_list': suplies,
        'equipments': equipments,
        'types': types
    }
    return render(request, template, context)


def edit(request,
         pk):
    suplies = Supply.all_objects.filter(deleted__isnull=True)
    equipments = Equipment.all_objects.filter(deleted__isnull=True)
    instance = Inventory.all_objects.get(
        deleted__isnull=True,
        pk=pk
    )
    form = InventoryForm(request.POST or None, instance=instance)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            messages.success(
                request, 'Se ha editado el inventario exitosamente')
            return redirect('internal:inventory.index')
        else:
            for field in form:
                if field.errors:
                    if field.name == 'name':
                        messages.error(
                            request,
                            'Ya existe un inventario con este nombre'
                        )
                    else:
                        msg = field.label + ': ' + str(field.errors)
                        messages.error(request, msg)

    inventories = Inventory.all_objects.filter(deleted__isnull=True)
    inventory_types = Inventory.TYPE_CHOICES
    types = []
    for type_aux in inventory_types:
        types.append(type_aux[1])
    context = {
        'inventories': inventories,
        'form': form,
        'inventory_types': inventory_types,
        'supply_list': suplies,
        'equipments': equipments,
        'inventory': instance,
        'types': types
    }
    template = 'internal/inventory/edit.html'
    return render(request, template, context)


def delete(request, pk):
    inventory = get_object_or_404(Inventory, pk=pk)
    inventory.delete()
    messages.success(request, 'Se ha borrado el inventario existosamente')
    return redirect('internal:inventory.index')


def show(request,
         pk):
    suplies = Supply.all_objects.filter(deleted__isnull=True)
    equipments = Equipment.all_objects.filter(deleted__isnull=True)
    instance = Inventory.all_objects.get(
        deleted__isnull=True,
        pk=pk
    )

    # get my articles
    inventory_articles = ArticleInventory.all_objects.filter(
        deleted__isnull=True,
        inventory=instance,
    )
    inventories = Inventory.all_objects.filter(deleted__isnull=True)
    inventory_types = Inventory.TYPE_CHOICES
    types = []
    for type_aux in inventory_types:
        types.append(type_aux[1])
    # if (instance.inventory_type=types[0]):
    #     suplies = inventory_articles.article

    context = {'inventories': inventories,
               'inventory_types': inventory_types,
               'inventory_articles': inventory_articles,
               'supply_list': suplies, 'equipments': equipments,
               'inventory': instance, 'types': types}
    template = 'internal/inventory/show.html'
    return render(request, template, context)


def save_article(request, pk):
    if request.is_ajax():
        if request.method == 'POST':
            # get values
            current_value = int(request.POST.get('current_value'))
            change_value = int(request.POST.get('change_value'))
            id = int(request.POST.get('id'))

            # get inventory and article
            inventory_types = Inventory.TYPE_CHOICES

            inventory = Inventory.all_objects.get(pk=pk)
            article_type = inventory.get_inventory_type_display()

            if (article_type == inventory_types[0][1]):  # insumos
                article = Supply.all_objects.get(pk=id)
            else:
                article = Equipment.all_objects.get(pk=id)

            # delete / update / create?
            if (current_value == 0):  # create
                newArticleInventory = ArticleInventory(
                    article=article, inventory=inventory, quantity=change_value)
                newArticleInventory.save()
            elif (current_value + change_value <= 0):  # delete
                oldArticleInventory = ArticleInventory.all_objects.get(inventory=inventory, article=article,
                                                                       deleted__isnull=True)
                oldArticleInventory.delete()
            else:  # update
                oldArticleInventory = ArticleInventory.all_objects.get(
                    inventory=inventory, article=article, deleted__isnull=True)
                oldArticleInventory.quantity = current_value + change_value
                oldArticleInventory.save()
            return HttpResponse(200)
