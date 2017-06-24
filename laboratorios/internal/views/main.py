from django.shortcuts import render
# from django.contrib.auth.decorators import login_required
# from django.utils.decorators import method_decorator
from internal.models import *

__all__ = (
    'index',
)


def index(request, template='internal/index.html'):
    context = {
        'method_list': [],
        'sample_data': {},
    }
    if hasattr(request.user, 'basicuser'):
        employee = Employee.all_objects.get(
            deleted__isnull=True,
            pk=request.user.basicuser.id
        )
        essay_method_fill_list = employee.assigned_essay_methods.all()
        essay_method_fill_list = EssayMethodFill.all_objects.filter(
            deleted__isnull=True,
            employees__in=[employee]
        )
        sample_data = {}
        for essay_method_fill in essay_method_fill_list:
            sample_data[essay_method_fill.id] = []
            sample = Sample.all_objects.get(
                deleted__isnull=True,
                pk=essay_method_fill.essay.sample.id
            )
            parameters_list = EssayMethodParameterFill.all_objects.filter(
                deleted__isnull=True,
                essay_method=essay_method_fill,
                value=''
            )
            sample_data[essay_method_fill.id].append({
                'sample': sample,
                'filled': not parameters_list.exists()
            })
        context = {
            'method_list': essay_method_fill_list,
            'sample_data': sample_data,
        }
    return render(request, template, context)
