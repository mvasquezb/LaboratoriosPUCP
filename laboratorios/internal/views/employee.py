from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from internal.models import *
from internal.views.forms import EmployeeForm


def index(request):
    return render(
        request,
        'internal/employee/index.html',
        {'users': Employee.objects.all()}
    )


def create(request,
           template='internal/employee/create.html'):
    form = EmployeeForm(request.POST or None)
    context = {
        'laboratories': Laboratory.objects.all(),
        'roles': Role.objects.all(),
    }
    if form.is_valid():
        form.save()
        return redirect('internal:employee.index')
    return render(request, template, context)


def edit(request, pk,
         template='internal/employee/edit.html'):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST, instance=employee)
    context = {
        'laboratories': Laboratory.objects.all(),
        'selected_laboratories': list(
            employee.laboratories.values_list('id', flat=True)
        ),
        'selected_roles': list(employee.role.values_list('id', flat=True)),
        'roles': Role.objects.all(),
        'custom_user': employee,
    }
    if form.is_valid():
        form.save()
        return redirect('internal:employee.index')
    return render(request, template, context)


def delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('internal:employee.index')
