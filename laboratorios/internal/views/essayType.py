from django.shortcuts import render,redirect,get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *

def index(request,
          template='internal/essayType/index.html',
          extra_context=None):
    types = EssayType.objects.all()
    context = {'essay_list': types}
    return render(request, template, context)

def validation_name(name):
    all_elements = EssayType.objects.all()
    for i in all_elements:
        if name==i.name:
            return False
    return True

def create(request,
          template='internal/essayType/create.html',
          extra_context=None):
    if  request.method == 'POST':
        index = 'internal/essayType/index.html'
        types = EssayType.objects.all()
        context = {'essay_list': types}
        if "b_cancel" in request.POST:
            return redirect('internal:essayType.index')
        if "b_submit" in request.POST:
            name = str(request.POST.get('text_essay_name'))
            if validation_name(name):
                description = str(request.POST.get('text_essay_description'))
                lab_type_choose = str(request.POST.get('comboBox_type'))
                lab_type = LaboratoryType.objects.get(name=lab_type_choose)
                if name:
                    essay_type = EssayType.objects.create(
                        name=name,
                        description=description,
                        active=True,
                        lab_type=lab_type
                    )
                    return redirect('internal:essayType.index')
            else:
                return redirect('internal:essayType.index')
    else:
        typelabs = LaboratoryType.objects.all()
        context = {'lab_types': typelabs}
        return render(request, template, context)

def edit(request,id):
    x = EssayType.objects.get(pk=id)
    print (x.name)
    typelabs = LaboratoryType.objects.all()
    context = {'essay': x,'lab_types':typelabs}
    template='internal/essayType/edit.html'
    return render(request, template, context)

def update(request,id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect('internal:essayType.index')
        if "b_submit" in request.POST:
            old_essay= EssayType.objects.get(pk=id)
            name = str(request.POST.get('text_essay_name'))
            description = str(request.POST.get('text_essay_description'))
            lab_type_choose = str(request.POST.get('comboBox_type'))
            lab_type = LaboratoryType.objects.get(name=lab_type_choose)
            old_essay.name=name
            old_essay.description=description
            old_essay.lab_type=lab_type
            old_essay.save()
            return redirect('internal:essayType.index')
    return redirect('internal:essayType.index')

def delete(request,
          template='internal/essayType/index.html',
          extra_context=None):
    print(request.GET)
    if request.method == 'GET':
        x = dict(request.GET)
        for i in x['array[]']:
            old = EssayType.objects.get(pk=i)
            old.active = False
            old.save()

    types = EssayType.objects.all()
    context = {'essay_list': types}
    return render(request, template, context)

