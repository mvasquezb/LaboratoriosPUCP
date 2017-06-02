from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from internal.models import TestTemplate
from internal.views.forms import *
from django.views.generic.list import ListView
from django.views.generic.edit import CreateView
from django.views.generic.edit import UpdateView
from django.views.generic.edit import DeleteView
from django.urls import *
from django.db import transaction
from django.forms import inlineformset_factory

# def index(request):
#     return render(request, 'internal/test/index.html', {'tests': TestTemplate.objects.all()})



class TestList(ListView):
    model = TestTemplate

class TestParameterCreate(CreateView):
    model = TestTemplate
    template_name = 'internal/test/create.html'
    fields = ['id', 'name']
    success_url = reverse_lazy('internal:test.index')


    def get_context_data(self, **kwargs):
        data = super(TestParameterCreate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['parameters'] = ParameterFormSet(self.request.POST)
        else:
            data['parameters'] = ParameterFormSet()
        data['title'] ="Crear Prueba"
        return data


    def form_valid(self, form):
        context = self.get_context_data()
        parameters = context['parameters']
        with transaction.atomic():
            self.object = form.save()

            if parameters.is_valid():
                parameters.instance = self.object
                parameters.save()
        return super(TestParameterCreate, self).form_valid(form)


class TestParameterUpdate(UpdateView):
    model = TestTemplate
    fields = ['id', 'name']
    template_name ='internal/test/create.html'
    success_url = reverse_lazy('internal:test.index')

    def get_context_data(self, **kwargs):
        data = super(TestParameterUpdate, self).get_context_data(**kwargs)
        if self.request.POST:
            data['parameters'] = ParameterFormSet(self.request.POST, instance=self.object)
        else:
            data['parameters'] = ParameterFormSet(instance=self.object)

        data['title'] = "Modificar Prueba"
        return data

    def form_valid(self, form):
        context = self.get_context_data()
        parameters = context['parameters']
        with transaction.atomic():
            self.object = form.save()

            if parameters.is_valid():
                parameters.instance = self.object
                parameters.save()
        return super(TestParameterUpdate, self).form_valid(form)


class TestDelete(DeleteView):
    model = TestTemplate
    template_name = 'internal/test/delete.html'
    success_url = reverse_lazy('internal:test.index')







def index(request,
          template='internal/test/index.html'):
    tests = TestTemplate.objects.all()
    data = {
        'object_list': tests,
    }
    return render(request, template, data)




# def create(request, template='internal/test/create.html'):
#     test = TestForm(request.POST or None, instance=test)
#     if form.is_valid():
#         form.save()
#         return redirect('internal:test.index')
#     return render(request, template, {'form': form})


# def edit(request,
#          pk,
#          template='internal/test/create.html'):
#     test = get_object_or_404(TestTemplate, pk=pk)
#     form = TestForm(request.POST or None, instance=test)
#     if form.is_valid():
#         form.save()
#         return redirect('internal:test.index')
#     return render(request, template, {'form': form})


def delete(request, pk, template='internal/test/delete.html'):
    test = get_object_or_404(TestTemplate, pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('internal:test.index')
    return render(request, template, {'test': test})


def store(request):
    context = {'message': 'Prueba creada exitosamente'}

    return redirect('internal:test.index')
