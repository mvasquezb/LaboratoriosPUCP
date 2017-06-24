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
from internal.views.forms import (
    EmployeeForm,
    UserCreationForm,
    UserEditForm
)
from django.contrib.auth.decorators import user_passes_test
import functools
from internal.permissions.employee import *


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
        'custom_employee': employee
    }
    return render(request, template, context)


@user_passes_test(create_employee_check, login_url='internal:index')
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


@user_passes_test(edit_employee_check, login_url='internal:index')
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


@user_passes_test(delete_employee_check, login_url='internal:index')
def delete(request, pk):
    employee = get_object_or_404(Employee, pk=pk)
    employee.delete()

    return redirect('internal:employee.index')


def samples_dashboard(request, template = 'internal/employee/samples_dashboard.html'):
    employee = Employee.objects.get(pk=request.user.basicuser.id)
    essay_method_fill_list = EssayMethodFill.objects.filter(request=employee).order_by('registered_date','id')
    sample_list = []
    for i in range(0,len(essay_method_fill_list[i])):
        sample = Sample.all_objects.get(deleted_isnull=True,pk=essay_method_fill_list[i].essay.sample.id)
        parameters_list = EssayMethodParameterFill.all_objects.filter(deleted__isnull=True,essay_method=essay_method_fill_list[i],value__isnull=True)
        sample_list.append({'sample':sample,
                            'filled':not parameters_list.exists()})
    context = {
        'methods_list':  essay_method_fill_list,
        'sample_list':essay_method_fill_forms
    }
    return render(request,template,context)
