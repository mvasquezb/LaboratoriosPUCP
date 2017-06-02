from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/testType/index.html',
          extra_context=None):
    types = TestType.objects.all().order_by('essay_type','name')
    context = {'test_list': types}
    return render(request, template, context)

def validation_name(name):
    all_elements = TestType.objects.all()
    for i in all_elements:
        if name==i.name:
            return False
    return True

def create(request,
          template='internal/testType/create.html',
          extra_context=None):
    if  request.method == 'POST':
        index = 'internal/testType/index.html'
        types = TestType.objects.all()
        context = {'test_list': types}
        if "b_cancel" in request.POST:
            return redirect('internal:testType.index')
        if "b_submit" in request.POST:
            name = str(request.POST.get('text_test_name'))
            description = str(request.POST.get('text_test_description'))
            essay_type_chosen = str(request.POST.get('comboBox_type'))
            essay_type = EssayType.objects.get(name=essay_type_chosen)
            if name:
                test_type = TestType.objects.create(
                    name=name,
                    description=description,
                    active=True,
                    essay_type=essay_type
                )
                return redirect('internal:testType.index')
            else:
                return redirect('internal:testType.index')
    else:
        typeEssay = EssayType.objects.all()
        context = {'essay_types': typeEssay}
        return render(request, template, context)

def edit(request,id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect('internal:testType.index')
        if "b_submit" in request.POST:
            old_test = TestType.objects.get(pk=id)
            name = str(request.POST.get('text_test_name'))
            description = str(request.POST.get('text_test_description'))
            essay_type_chosen = str(request.POST.get('comboBox_type'))
            essay_type = EssayType.objects.get(name=essay_type_chosen)
            old_test.name = name
            old_test.description = description
            old_test.essay_type = essay_type
            old_test.save()
            return redirect('internal:testType.index')
        return redirect('internal:testType.index')
    else:
        x = TestType.objects.get(pk=id)
        print (x.name)
        typeEssay = EssayType.objects.all()
        context = {'test': x,'essay_types':typeEssay}
        template='internal/testType/edit.html'
        return render(request, template, context)

def delete(request,
          template='internal/testType/index.html',
          extra_context=None):
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            old = TestType.objects.get(pk=i)
            old.active = False
            old.save()

    types = TestType.objects.all()
    context = {'test_list': types}
    return render(request, template, context)

