from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from django.contrib import messages
from internal.models import *
from internal.views.forms import *
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import *
from django.db import transaction
from django.forms import inlineformset_factory

def index(request):
    return render(request, 'internal/servicerequest/index.html', {'requests': ServiceRequest.objects.all()})


def create(request,
           pk,
           template='internal/servicerequest/create.html'):
    selected_client = Client.objects.get(pk=pk)
    service_request_form = ServiceRequestForm(request.POST or None,initial={'client':selected_client})
    context = {'sr_form': service_request_form,'pk':pk}
    if service_request_form.is_valid():
         created_service_request = service_request_form.save()
         messages.success(request, 'Se ha creado la solicitud exitosamante!')
         return redirect(reverse('internal:servicerequest.index'))
    return render(request, template, context)


def select_client(request, template='internal/servicerequest/select_client.html'):
    types = Client.objects.all().order_by('doc_number', 'username')
    context = {'client_list': types}
    return render(request, template, context)

def create_client(request,
           template='internal/servicerequest/create_client.html'):
    form = ClientForm(request.POST or None)
    context = {'form':form}
    if form.is_valid():
        new_client = form.save()
        return redirect(reverse('internal:servicerequest.create', args=(new_client.pk,)))
    return render(request, template, context)

def edit(request,
    pk,
    template ='internal/servicerequest/edit.html'):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request_form = ServiceRequestForm(request.POST or None, instance=service_request)
    #For all samples and their selected essayFills in list
    sample_list=Sample.objects.filter(request=service_request)
    essay_fill_list=[]
    essay_methods_list=[] # To get all essay_methods for every sample
    essay_methods_chosen_forms=[] # To get whether each essay_method is chosen or not  
    
    for i in range(0,len(sample_list)):
        sample_listed = sample_list[i]
        essay_fill = EssayFill.objects.filter(sample=sample_listed)[0]
        essay_fill_list.append(essay_fill)
        essay_methods_list.append(EssayMethodFill.objects.filter(essay=essay_fill))
        aux_essay_methods_forms=[]
        for j in range(0,len(essay_methods_list[i])):
            aux_essay_methods_forms.append(EssayMethodFillChosenForm(request.POST or None, instance=essay_methods_list[i][j], prefix='emf_'+str(essay_methods_list[i][j].id)))
        essay_methods_chosen_forms.append(aux_essay_methods_forms) 
    
    context = {'form':service_request_form,'samples':sample_list,'essays':essay_fill_list,'essays_methods':essay_methods_list,'essay_methods_chosen_forms':essay_methods_chosen_forms,'pk':pk}
    # verificacion
    forms_verified = 0 # Means true lol

    # loop for verifying each essay method form
    for i in range(0,len(essay_methods_chosen_forms)):
        for j in range(0,len(essay_methods_chosen_forms[i])):
            if essay_methods_chosen_forms[i][j].is_valid():
                pass
            else:
                forms_verified +=1
    if service_request_form.is_valid():
        pass
    else:
        forms_verified +=1
    # end of verifying segment        

    if forms_verified == 0:
        service_request_form.save()
        # add save for each form 
        for i in range(0,len(essay_methods_chosen_forms)):
            for j in range(0,len(essay_methods_chosen_forms[i])):
                essay_methods_chosen_forms[i][j].save()
        return redirect(reverse("internal:servicerequest.index"))
    return render(request, template, context)




def add_sample(request,
    pk,
    template='internal/servicerequest/add_sample.html'):
    service_request = ServiceRequest.objects.get(pk=pk)
    sample_form = SampleForm(request.POST or None, initial={'request':service_request,})
    context = {'form':sample_form,'pk':pk}
    # verificacion
    if sample_form.is_valid():
        sample_form.save()    
        return redirect(reverse("internal:servicerequest.edit",args=(pk,)))
    return render(request, template, context)


def edit_sample(request,
    pk_request,
    pk_sample,
    template='internal/servicerequest/edit_sample.html'):
    sample = Sample.objects.get(pk=pk_sample)
    sample_form = SampleEditForm(request.POST or None, instance = sample)
    essay_fill_form = EssayFillSelectionForm(request.POST or None, instance = EssayFill.objects.get(sample=sample))
    forms = [sample_form,essay_fill_form]
    context = {'forms':forms,'pk_request':pk_request,'pk_sample':pk_sample}
    if sample_form.is_valid() and essay_fill_form.is_valid():
        sample_form.save()
        essay_fill_form.save()
        return redirect(reverse("internal:servicerequest.edit",args=(pk_request,)))
    return render(request, template, context)

def delete(request,
    pk):
    service_request = ServiceRequest.objects.get(pk=pk)
    service_request.delete()
    return redirect(reverse("internal:servicerequest.index"))

def delete_sample(request,
    pk_request,
    pk_sample):
    sample = Sample.objects.get(pk=pk_sample)
    sample.delete()
    return redirect(reverse("internal:servicerequest.edit",args=(pk_request,)))    