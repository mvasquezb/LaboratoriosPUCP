from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/essayTemplate/index.html',
          extra_context=None):
    types = EssayTemplate.objects.all().order_by('lab_type', 'name')
    context = {'essay_list': types}
    return render(request, template, context)


def create(request,
           template='internal/essayTemplate/create.html',
           extra_context=None):
    if request.method == 'POST':
        types = EssayTemplate.objects.all()
        context = {'essay_list': types}
        if "b_cancel" in request.POST:
            return redirect('internal:essayTemplate.index')
        if "b_submit" in request.POST:
            name = str(request.POST.get('text_essay_name'))
            if not EssayTemplate.objects.filter(name=name).exists():
                description = str(request.POST.get('text_essay_description'))
                lab_type_chosen = str(request.POST.get('comboBox_type'))
                lab_type = LaboratoryType.objects.get(name=lab_type_chosen)
                if name:
                    essay_type = EssayTemplate.objects.create(
                        name=name,
                        description=description,
                        active=True,
                        lab_type=lab_type
                    )
                    return redirect('internal:essayTemplate.create')
            else:
                return redirect('internal:essayTemplate.index')
    else:
        typelabs = LaboratoryType.objects.all()
        context = {'lab_types': typelabs}
        return render(request, template, context)


def edit(request, id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect('internal:essayTemplate.index')
        if "b_submit" in request.POST:
            old_essay = EssayTemplate.objects.get(pk=id)
            name = str(request.POST.get('text_essay_name'))
            description = str(request.POST.get('text_essay_description'))
            lab_type_chosen = str(request.POST.get('comboBox_type'))
            lab_type = LaboratoryType.objects.get(name=lab_type_chosen)
            old_essay.name = name
            old_essay.description = description
            old_essay.lab_type = lab_type
            old_essay.save()
            return redirect('internal:essayTemplate.index')
        return redirect('internal:essayTemplate.index')
    else:
        essay = EssayTemplate.objects.get(pk=id)
        typelabs = LaboratoryType.objects.all()
        context = {'essay': essay, 'lab_types': typelabs}
        template = 'internal/essayTemplate/edit.html'
        return render(request, template, context)


def delete(request,
           template='internal/essayTemplate/index.html',
           extra_context=None):
    if request.method == 'GET':
        array_pk = dict(request.GET)
        for i in array_pk['array[]']:
            old = EssayTemplate.objects.get(pk=i)
            old.active = False
            old.save()

    types = EssayTemplate.objects.all()
    context = {'essay_list': types}
    return render(request, template, context)
