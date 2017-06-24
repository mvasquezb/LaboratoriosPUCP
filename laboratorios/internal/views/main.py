from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from internal.models import *

__all__ = (
    'index',
)


def index(request, template='internal/index.html'):
    if hasattr(request.user, 'basicuser'):
        employee = Employee.all_objects.get(
            deleted__isnull=True,
            pk=request.user.basicuser.id
        )
        essay_method_fill_list = employee.assigned_essay_methods.all()[::1]
        print(essay_method_fill_list)
        sample_list = []
        for essay_method_fill in essay_method_fill_list:
            sample = Sample.all_objects.get(
                deleted__isnull=True,
                pk=essay_method_fill.essay.sample.id
            )
            print(sample)
            parameters_list = EssayMethodParameterFill.all_objects.filter(
                deleted__isnull=True,
                essay_method=essay_method_fill
            )
            print(parameters_list)
            sample_list.append({
                'sample': sample,
                'filled': not parameters_list.exists()
            })
        context = {
            'methods_list': essay_method_fill_list,
            'samples_list': sample_list
        }
    else:
        context = {
            'methods_list': [],
            'samples_list': []
        }
    return render(request, template, context)
