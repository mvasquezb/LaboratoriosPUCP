from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from ..models import *


def index(request,
          template='internal/laboratory/index.html',
          extra_context=None):
    if request.method == 'GET' and request.is_ajax():
        x = dict(request.GET)
        for i in x['array[]']:
            print(i)
            print('  ')
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)


def create(request,
           template='internal/laboratory/create.html',
           extra_context=None):
    if request.method == 'POST':
        name = str(request.POST.get('textname'))
        numberUsers = int(request.POST.get('numberUsers'))
        capacity2 = 0
        lab_type_list = str(request.POST.get('comboBox_type'))
        lab_type = LaboratoryType.objects.get(name=lab_type_list)
        if name:
            lab = Laboratory.objects.create(
                name=name,
                users_number=numberUsers,
                capacity=capacity2,
                active=True,
                type=lab_type
            )
        return redirect('internal:laboratory.index')
    else:
        typelabs = LaboratoryType.objects.all()
        users = User.objects.all()
        context = {'types': typelabs, 'users': users}
        return render(request, template, context)


def delete(request,
           template='internal/laboratory/index.html',
           extra_context=None):
    if request.method == 'GET' and request.is_ajax():
        x = dict(request.GET)
        for i in x['array[]']:
            Laboratory.objects.filter(pk=i).delete()


def edit(request, id_lab):
    if request.method == 'POST':
        if "cancelButton" in request.POST:
            return redirect('internal:laboratory.index')
        if "createButton" in request.POST:
            old_lab = Laboratory.objects.get(pk=id_lab)
            name = str(request.POST.get('textname'))
            numberUsers = int(request.POST.get('numberUsers'))
            capacity2 = 0
            lab_type_list = str(request.POST.get('comboBox_type'))
            lab_type = LaboratoryType.objects.get(name=lab_type_list)
            old_lab.name = name
            old_lab.capacity = capacity2
            old_lab.users_number = numberUsers
            old_lab.type = lab_type
            old_lab.save()
            return redirect('internal:laboratory.index')
    else:
        lab = Laboratory.objects.get(pk=id_lab)
        typelabs = LaboratoryType.objects.all()
        context = {'lab': lab, 'types': typelabs}
        template = 'internal/laboratory/edit.html'
        return render(request, template, context)


def getMonitorId(MonitorStr):
    returnId = 1
    for character in MonitorStr:
        if (character == ' '):
            break
        returnId = returnId * 10 + int(character)
    return returnId

def assignMonitor(request, id):
    if request.method == 'POST':
        if "b_cancel" in request.POST:
            return redirect('internal:laboratory.index')
        if "b_submit" in request.POST:
            modifyingLaboratory = Laboratory.objects.get(pk=id)
            newMonitorStr = str(request.POST.get('comboBox_users'))
            newMonitorId = getMonitorId(newMonitorStr)
            newMonitor = User.objects.get(pk = newMonitorId)
            modifyingLaboratory.monitor = newMonitor
            modifyingLaboratory.save()
            return redirect('internal:laboratory.index')
        return redirect('internal:laboratory.index')
    else:
        labo = Laboratory.objects.get(pk=id)
        userList = User.objects.all()
        context = {'laboratory': labo, 'users': userList}
        template = 'internal/laboratory/assignmonitor.html'
        return render(request, template, context)
