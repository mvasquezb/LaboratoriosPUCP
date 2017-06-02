from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/testTemplate/index.html',
          extra_context=None):
    types = TestTemplate.objects.all().order_by('essay_template', 'name')
    context = {'test_list': types}
    return render(request, template, context)


def create(request,
           template='internal/testTemplate/create.html',
           extra_context=None):
    if request.method == 'POST':
        types = TestTemplate.objects.all()
        context = {'test_list': types}
        if "b_cancel" in request.POST:
            return redirect('internal:testTemplate.index')
        if "b_submit" in request.POST:
            name = str(request.POST.get('text_test_name'))
            description = str(request.POST.get('text_test_description'))
            essay_type_chosen = str(request.POST.get('comboBox_type'))
            essay_type = EssayTemplate.objects.get(name=essay_type_chosen)
            if name:
                test_type = TestTemplate.objects.create(
                    name=name,
                    description=description,
                    active=True,
                    essay_template=essay_type
                )
                return redirect('internal:testTemplate.create')
            else:
                return redirect('internal:testTemplate.index')
    else:
        typeEssay = EssayTemplate.objects.all()
        context = {'essay_types': typeEssay}
        return render(request, template, context)


def edit(request, id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect('internal:testTemplate.index')
        if "b_submit" in request.POST:
            old_test = TestTemplate.objects.get(pk=id)
            name = str(request.POST.get('text_test_name'))
            description = str(request.POST.get('text_test_description'))
            essay_type_chosen = str(request.POST.get('comboBox_type'))
            essay_type = EssayTemplate.objects.get(name=essay_type_chosen)
            old_test.name = name
            old_test.description = description
            old_test.essay_template = essay_type
            old_test.save()
            return redirect('internal:testTemplate.index')
        return redirect('internal:testTemplate.index')
    else:
        x = TestTemplate.objects.get(pk=id)
        print(x.name)
        typeEssay = EssayTemplate.objects.all()
        context = {'test': x, 'essay_types': typeEssay}
        template = 'internal/testTemplate/edit.html'
        return render(request, template, context)


def delete(request,
           template='internal/testTemplate/index.html',
           extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            old = TestTemplate.objects.get(pk=i)
            old.active = False
            old.save()

    types = TestTemplate.objects.all()
    context = {'test_list': types}
    return render(request, template, context)
