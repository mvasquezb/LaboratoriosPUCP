from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from internal.models import *

__all__ = (
    'index',
)


def index(request, template = 'internal/index.html'):
    if hasattr(request.user, 'basicuser'):
        employee = Employee.objects.get(pk=request.user.basicuser.id)
        essay_method_fill_list = employee.assigned_essay_methods.all()
        sample_list = []
        for i in range(0,len(essay_method_fill_list)):
            sample = Sample.all_objects.get(deleted__isnull=True,pk=essay_method_fill_list[i].essay.sample.id)
            parameters_list = EssayMethodParameterFill.all_objects.filter(deleted__isnull=True,essay_method=essay_method_fill_list[i],value__isnull=True)
            sample_list.append({'sample':sample,
                            'filled':not parameters_list.exists()})
        context = {
            'methods_list':  essay_method_fill_list,
            'samples_list':sample_list
        }
    context = { 
        'methods_list':  [],
            'samples_list': []
    }
    return render(request,template,context)
