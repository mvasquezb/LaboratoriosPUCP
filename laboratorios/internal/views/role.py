from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from internal.models import Role
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
    if form.is_valid():
        form.save()
        return redirect('internal:role.index')
    return render(request, template, {'form': form})


def edit(request,
         pk,
         template='internal/role/create.html'):
    role = get_object_or_404(Role, pk=pk)
    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return redirect('internal:server_list')
    return render(request, template, {'form': form})


def delete(request, pk, template='internal/role/delete.html'):
    role = get_object_or_404(Role, pk=pk)
    if request.method == 'POST':
        role.delete()
        return redirect('internal:role.index')
    return render(request, template, {'role': role})
