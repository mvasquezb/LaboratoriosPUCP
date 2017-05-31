from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from internal.models import *
from internal.views.forms import UserForm

def index(request):
    return render(request, 'internal/user/index.html', {'users': User.objects.all()})


def create(request,
           template='internal/user/create.html'):
    form = UserForm(request.POST or None)
    context={
        'laboratories' : Laboratory.objects.all(),
        'roles' : Role.objects.all(),
    }
    if form.is_valid():
        form.save()
        return redirect('internal:user.index')
    return render(request, template, context)


def edit(request, pk,
           template='internal/user/edit.html'):
    user = get_object_or_404(User, pk=pk)
    form = UserForm(request.POST or None, instance=user)
    context={
        'laboratories' : Laboratory.objects.all(),
        'selected_laboratories' : list(user.laboratories.values_list('id', flat=True)),
        'selected_roles' : list(user.role.values_list('id', flat=True)),
        'roles' : Role.objects.all(),
        'custom_user' : user,
    }
    if form.is_valid():
        form.save()
        return redirect('internal:user.index')
    return render(request, template, context)


def delete(request, pk):
    user = get_object_or_404(User, pk=pk)
    user.delete()

    return redirect('internal:user.index')