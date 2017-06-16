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
from django.contrib.auth.decorators import login_required
from internal.views.forms import (
    EmployeeForm,
    UserCreationForm,
    UserEditForm
)


def index(request,
          template='internal/employee/index.html',
          extra_context=None):
    employee_list = Employee.objects.order_by('user__username')

    context = {
        'employees_list': employee_list,
    }
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)


def show(request,
         pk,
         template='internal/employee/show.html'):
    employee = get_object_or_404(Employee, pk=pk)
    context = {
        'selected_laboratories': employee.laboratories.all(),
        'selected_roles': employee.roles.all(),
        'employee': employee
    }
    return render(request, template, context)


def create(request,
           template='internal/employee/create.html'):
    user_form = UserCreationForm(request.POST or None)
    form = EmployeeForm(request.POST or None)
    context = {
        'laboratories': Laboratory.all_objects.filter(deleted__isnull=True),
        'roles': Role.all_objects.filter(deleted__isnull=True),
        'form': form,
        'user_form': user_form,
    }
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            new_user = user_form.save()
            form.instance.user = new_user
            new_employee = form.save()
            messages.success(
                request,
                'Se ha creado el empleado exitosamante!'
            )
            return redirect('internal:employee.index')
        else:
            # Show errors
            pass
    return render(request, template, context)


def edit(request, pk,
         template='internal/employee/edit.html'):
    employee = get_object_or_404(Employee, pk=pk)
    user_form = UserEditForm(request.POST or None, instance=employee.user)
    form = EmployeeForm(request.POST or None, instance=employee)
    context = {
        'laboratories': Laboratory.all_objects.filter(deleted__isnull=True),
        'selected_laboratories': employee.laboratories.all(),
        'selected_roles': employee.roles.all(),
        'roles': Role.all_objects.filter(deleted__isnull=True),
        'form': form,
        'custom_employee': employee,
        'user_form': user_form,
    }
    if request.method == 'POST':
        if user_form.is_valid() and form.is_valid():
            user_form.save()
            form.save()
            messages.success(request, 'Se ha editado el empleado exitosamante!')
            return redirect('internal:employee.index')
        else:
            print(user_form.errors, form.errors)
            messages.warning(request, 'Please correct the error below.')
    return render(request, template, context)


def delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('internal:employee.index')
