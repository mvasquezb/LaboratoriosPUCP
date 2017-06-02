from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from internal.models  import *
from internal.views.forms import RoleForm




def index(request,
          template='internal/role/index.html'):
    roles = Role.objects.all()
    data = {
        'object_list': roles,
    }
    
    return render(request, template, data)


def create(request,
           template='internal/role/create.html'):
    form = RoleForm(request.POST or None)
    print(form.errors)
    if form.is_valid():
        role = form.save(commit=False)
        role.save()
        form.save_m2m()
        return redirect('internal:role.index')
    return render(request, template, {'form': form})


def edit(request,
         pk,
         template='internal/role/edit.html'):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    context = {
        'accesses' : Access.objects.all(),
        'selected_accesses' : list(
            role.access.values_list('id', flat=True)
        ),
        'custom_role' : role
    }
    if form.is_valid():
        form.save()
        return redirect('internal:role.index')
    return render(request, template, context)


def delete(request, pk):
    role = get_object_or_404(Role, pk=pk)
    role.delete()

    return redirect('internal:role.index')
