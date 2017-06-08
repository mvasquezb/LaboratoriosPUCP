from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from internal.models import *
from internal.views.forms import EmployeeForm
from internal.views.forms import RoleForm
def index(request, template='internal/role/index.html',extra_context=None):
    search=request.GET.get('search')
    if search:
        role_list = Role.objects.filter(name__icontains=search).order_by('name')
    else:
        role_list = Role.objects.order_by('name')

    paginator = Paginator(role_list,3)
    page=request.GET.get('page')
    try:
        roles=paginator.page(page)
    except PageNotAnInteger:
        roles=paginator.page(1)
    except EmptyPage:
        roles=paginator.page(paginator.num_pages)
    context = {
        'role_list': roles,
        'paginator':paginator
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)

def show(request, pk, template='internal/role/show.html'):
    role = get_object_or_404(Role, pk=pk)
    context = {
        'selected_permissions':role.permissions.all(),
        'role':role
    }
    return render(request, template, context)

def create(request,
           template='internal/role/create.html'):
    form = RoleForm(request.POST or None)
    context = {
        'permissions': Permission.objects.all(),
        'form': form
    }
    if request.method == 'POST':
        if form.is_valid():
            new_role = form.save(commit=False)
            new_role.save()
            form.save_m2m()
            messages.success(request, 'Se ha creado el rol correctamente')
            return redirect('internal:role.index')
    return render(request,template,context)

def edit(request, pk,
         template='internal/role/edit.html'):
    role=get_object_or_404(Role,pk=pk)
    form = RoleForm(request.POST or None,instance=role)
    context = {
        'permissions': Permission.objects.all(),
        'selected_permissions': role.permissions.all(),
        'form':form,
        'custom_role':role,
    }
    if request.method == 'POST':
        print(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'se ha editadod con exito')
            return redirect('internal:role.index')
        else:
            messages.warning(request,'por favor corregir')
    return render(request,template,context)

def delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    role.delete()
    return redirect('internal:role.index')