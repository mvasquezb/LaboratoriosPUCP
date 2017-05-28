from django.shortcuts import render,redirect, get_object_or_404
from django.forms import ModelForm
from django.http import HttpResponse, HttpResponseRedirect
from internal.models import Role


class RoleForm(ModelForm):
    class Meta:
        model = Role
        fields = ['description', 'access']

def role_list(request,template_name = 'internal/role/role_list.html'):
    roles = Role.objects.all()
    data = {}
    data['object_list']= roles
    return render(request, template_name, data)

def role_create(request, template_name= 'internal/role/role_form.html'):
    form = RoleForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('role_list')
    return render(request, template_name, {'form':form})

def role_update(request, pk, template_name='internal/role/role_form.html'):
    role = get_object_or_404(Role, pk = pk)
    form = RoleForm(request.POST or None, instance=role)
    if form.is_valid():
        form.save()
        return redirect('server_list')
    return render(request, template_name,{'form':form})

def role_delete(request, pk, template_name='internal/role/role_confirm_delete.html'):
    role = get_object_or_404(Role,pk = pk)
    if request.method=='POST':
        role.delete()
        return redirect('role_list')
    return render(request, template_name, {'object': role})

