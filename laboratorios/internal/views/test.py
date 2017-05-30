from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)

from internal.models import TestTemplate
from internal.views.forms import TestForm


# def index(request):
#     return render(request, 'internal/test/index.html', {'tests': TestTemplate.objects.all()})

def index(request,
          template='internal/test/index.html'):
    tests = TestTemplate.objects.all()
    data = {
        'object_list': tests,
    }
    return render(request, template, data)


def create(request, template='internal/test/create.html'):
    form = TestForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('internal:test.index')
    return render(request, template, {'form': form})


def edit(request,
         pk,
         template='internal/test/create.html'):
    test = get_object_or_404(TestTemplate, pk=pk)
    form = TestForm(request.POST or None, instance=test)
    if form.is_valid():
        form.save()
        return redirect('internal:test.index')
    return render(request, template, {'form': form})


def delete(request, pk, template='internal/test/delete.html'):
    test = get_object_or_404(TestTemplate, pk=pk)
    if request.method == 'POST':
        test.delete()
        return redirect('internal:test.index')
    return render(request, template, {'test': test})


def store(request):
    context = {'message': 'Prueba creada exitosamente'}

    return redirect('internal:test.index')
