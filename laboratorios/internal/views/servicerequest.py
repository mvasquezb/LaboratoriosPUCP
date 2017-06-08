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
    essay_methods_active=[] # To get whether each essay_method is chosen or not  
    
    for i in range(0,len(sample_list)):
        sample_listed = sample_list[i]
        essay_fill = EssayFill.objects.filter(sample=sample_listed)[0]
        essay_fill_list.append(essay_fill)
        essay_methods_list.append(EssayMethodFill.objects.filter(essay=essay_fill))

        aux_active_list=[]

        # Logic for samples dashboard for each user
        # for j in range(0,len(essay_methods_list[i])):
        #     if len(essay_methods_list[i][j].employees.all())>0:
        #         aux_active_list.append('X')
        #     else:
        #         aux_active_list.append('_')

        for j in range(0,len(essay_methods_list[i])):
            if essay_methods_list[i][j].chosen is True:
                aux_active_list.append('X')
            else:
                aux_active_list.append('_')
        essay_methods_active.append(aux_active_list) 
    
    context = {'form':service_request_form,'samples':sample_list,'essays':essay_fill_list,'essays_methods':essay_methods_list,'essays_methods_active':essay_methods_active,'pk':pk}
    # verificacion
    if service_request_form.is_valid():
        service_request_form.save()
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



    # def add_sample(request,
    # pk,
    # template='internal/servicerequest/add_sample.html'):
    # service_request = ServiceRequest.objects.get(pk=pk)
    # if (len(Sample.objects.filter(request=service_request))==0):
    #     sample_form = SampleForm(request.POST or None, initial={'request':service_request,})
    # else:
    #     sample_previous = Sample.objects.filter
    #     sample_form = SampleForm(request.POST or None, initial={'request':service_request,})
    # active_list = []
    # essay_methods_list =[]
    # #For all samples and their selected essayFills in list
    # if len(EssayFill.objects.filter(sample=pk))>0:
    #     essay = EssayFill.objects.filter(sample=pk)[0]
    #     if len(EssayMethodFill.objects.filter(essay=essay))>0: 
    #         essay_methods_list = EssayMethodFill.objects.filter(essay=essay)   
    #         for i in range(0,len(essay_method_list)):
    #             if essay_methods_list[i].chosen is True:
    #                 active_list.append('X')
    #             else:
    #                 active_list.append('_')
 
    # context = {'form':sample_form,'essay_methods':essay_methods_list,'active_list':active_list,'pk':pk}
    # # verificacion
    # if sample_form.is_valid():
    #     sample = service_request_form.save()
    #     essay_selected = self.cleaned_data['essay_field']
    #     # If there is no previous selection for essay or it has been changed
    #     if (len(EssayFill.objects.filter(sample=sample)) == 0 or len(EssayFill.objects.filter(sample=sample,pk=sample)) == 0):
    #         essay_fill_created = EssayFill(sample=sample)
    #         essay_fill_created.create(essay_selected)
    #         essay_fill_created.save()    
    #     return redirect(reverse("internal:servicerequest.edit",args=(pk,)))
    # return render(request, template, context)