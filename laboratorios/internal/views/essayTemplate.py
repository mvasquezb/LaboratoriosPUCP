from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from internal.models import *
from internal.views.forms import EssayTemplateForm

def index(request):
    return render(request, 'internal/essayTemplate/index.html', {'essays': EssayTemplate.objects.all()})


def create(request,
           template='internal/essayTemplate/create.html'):
    form = EssayTemplateForm(request.POST or None)
    context={
        'tests' : TestTemplate.objects.all(),
    }
    print(form.errors)

    if form.is_valid():
        form.save()
        print(form.data)
        return redirect('internal:essayTemplate.index')
    return render(request, template, context)


def edit(request, pk,
           template='internal/essayTemplate/edit.html'):
    essay = get_object_or_404(EssayTemplate, pk=pk)
    form = EssayTemplateForm(request.POST or None, instance=essay)
    context={
        'tests' : TestTemplate.objects.all(),
        'selected_tests' : list(essay.tests.all().values_list('id', flat=True)),
        'custom_essay' : essay,
    }

    if form.is_valid():
        form.save()
        return redirect('internal:essayTemplate.index')
    return render(request, template, context)


def delete(request, pk):
    essay = get_object_or_404(EssayTemplate, pk=pk)
    essay.delete()

    return redirect('internal:essayTemplate.index')
