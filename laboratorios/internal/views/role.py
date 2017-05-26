from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import TemplateView,ListView
from django.views.generic.edit import CreateView, UpdateView,DeleteView
from django.core.urlresolvers import  reverse_lazy

from .models import Role

class RoleList(ListView):
    model = Role

class RoleCreate(CreateView):
    model = Role
    success_url = reverse_lazy('role_list')
    fields = ['description']

class RoleUpdate(UpdateView):
    model = Role
    success_url = reverse_lazy('role_list')
    fields = ['description']

class RoleDelete(DeleteView):
    model = Role
    success_url = reverse_lazy('role_list')
    fields = ['description']
