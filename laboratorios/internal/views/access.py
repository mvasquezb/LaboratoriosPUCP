from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from internal.models import Access
from internal.views.forms import AccessForm


def index(request,
          template='internal/access/index.html'):
    accesses = Access.objects.all()
    data = {
        'object_list': accesses,
    }
    return render(request, template, data)


def create(request,
           template='internal/access/create.html'):
    form = AccessForm(request.POST or None)
    print(form.errors)
    if form.is_valid():
        role = form.save(commit=False)
        role.save()
        form.save_m2m()
        return redirect('internal:access.index')
    return render(request, template, {'form': form})


def edit(request,
         pk,
         template='internal/access/create.html'):
    access = get_object_or_404(Access, pk=pk)
    form = AccessForm(request.POST or None, instance=access)
    if form.is_valid():
        form.save()
        return redirect('internal:access.index')
    return render(request, template, {'form': form})


def delete(request, pk, template='internal/access/delete.html'):
    access = get_object_or_404(Access, pk=pk)
    if request.method == 'POST':
        access.delete()
        return redirect('internal:access.index')
    return render(request, template, {'object': access})
