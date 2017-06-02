from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from internal.models import *
from internal.views.forms import *
from django.views.generic import *
from django.urls import *
from django.db import transaction



class ServiceRequestList(ListView):
    model = ServiceRequest

class RequestServiceSampleCreate(CreateView):
    model = ServiceRequest
    template_name = 'internal/servicerequest/create.html'
    fields = ['description']
    success_url = reverse_lazy('internal:servicerequest.index')


    def get_context_data(self, **kwargs):
        data = super(RequestServiceSampleCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['samples'] = SampleFormSet(self.request.POST)
        else:
            data['samples'] = SampleFormSet()
        data['title'] ="Creación de Solicitud: Completar detalles"
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        samples = context['samples']
        with transaction.atomic():
            self.object = form.save()

            if samples.is_valid():
                samples.instance = self.object
                samples.save()
        return super(RequestServiceSampleCreate, self).form_valid(form)



































def index(request):
    return render(request, 'internal/servicerequest/index.html', {'requests': ServiceRequest.objects.all()})


def create(request,
           pk,
           template='internal/servicerequest/create.html'):
    selected_client = Client.objects.get(pk=pk)
    form = ServiceRequestForm(request.POST or None,initial={'client':selected_client})
    context = {'form': form,'pk':pk }
    if form.is_valid():
        form.save()
        return redirect(reverse('internal:servicerequest.index'))
    return render(request, template, context)


def store(request):
    context = {'message': 'Solicitud creada exitosamente'}
    return redirect('internal:servicerequest.index')


def select_client(request, template='internal/servicerequest/select_client.html'):
    types = Client.objects.all().order_by('idDoc', 'name')
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
