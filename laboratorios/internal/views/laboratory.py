from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from internal.models import Laboratory


def index(request,
          template='internal/laboratory/index.html',
          extra_context=None):
    labs = Laboratory.objects.all()
    context = {'lab_list': labs}
    return render(request, template, context)


def create(request,
           template='internal/laboratory/create.html',
           extra_context=None):
    if request.method == 'POST':
        name = str(request.POST.get('textname'))
        numberUsers = int(request.POST.get('numberUsers'))
        capacity2 = int(request.POST.get('text_capacity'))
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
        return HttpResponse("Laboratorio de " + name + str(numberUsers) + str(capacity2) + "tipo: " + str(lab_type_list) + "Creado exitosamente")
    else:
        typelabs = LaboratoryType.objects.all()
        context = {'types': typelabs}
        return render(request, template, context)
