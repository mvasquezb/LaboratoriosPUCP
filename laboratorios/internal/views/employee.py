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

def index(request):
    search = request.GET.get('search')
    if search:        
        employee_list = Employee.objects.filter(username__icontains=search).order_by('username')
    else:
        employee_list = Employee.objects.order_by('username')
    paginator = Paginator(employee_list, 3)
    page = request.GET.get('page')
    try:
        employees = paginator.page(page)
    except PageNotAnInteger:
        employees = paginator.page(1)
    except EmptyPage:
        employees = paginator.page(paginator.num_pages)

    return render(request, 'internal/employee/index.html', {'employees_list': employees})


def detail(request, pk,
           template='internal/employee/detail.html'):
    employee = get_object_or_404(Employee, pk=pk)

    return render(request, 'internal/employee/index.html', {'employee': employee})


def create(request,
           template='internal/employee/create.html'):
    form = EmployeeForm(request.POST or None)
    context={
        'laboratories' : Laboratory.objects.all(),
        'roles' : Role.objects.all(),
        'form' : form
    }
    if form.is_valid():
        form.save()
        return redirect('internal:employee.index')
    return render(request, template, context)


def edit(request, pk,
           template='internal/employee/edit.html'):
    employee = get_object_or_404(Employee, pk=pk)
    form = EmployeeForm(request.POST or None, instance=employee)
    context={
        'laboratories' : Laboratory.objects.all(),
        'selected_laboratories' : list(employee.laboratories.values_list('id', flat=True)),
        'selected_roles' : list(employee.roles.values_list('id', flat=True)),
        'roles' : Role.objects.all(),
        'form' : form,
        'custom_employee' : employee,
    }
    if form.is_valid():
        form.save()
        messages.success(request, 'Your password was updated successfully!')
        return redirect('internal:employee.index')
    else:
        messages.warning(request, 'Please correct the error below.')
    return render(request, template, context)


def delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('internal:employee.index')