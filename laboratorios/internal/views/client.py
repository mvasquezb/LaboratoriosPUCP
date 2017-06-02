from django.shortcuts import (
    render,
    get_object_or_404,
    redirect,
    reverse,
    HttpResponseRedirect
)
from internal.models import *
from internal.views.forms import ClientForm

def index(request):
    return render(request, 'internal/client/index.html', {'clients': Client.objects.all()})


def create(request,
           template='internal/client/create.html'):
    form = ClientForm(request.POST or None)
    print(form.errors)
    if form.is_valid():
        form.save()
        return redirect('internal:client.index')
    return render(request, template, {'form': form})


def edit(request, pk,
           template='internal/client/edit.html'):
    client = get_object_or_404(Client, pk=pk)
    form = ClientForm(request.POST or None, instance=client)
    context={
        'current_client' : client,
    }
    if form.is_valid():
        form.save()
        return redirect('internal:client.index')
    return render(request, template, context)


def delete(request, pk):
    client= get_object_or_404(Client, pk=pk)
    client.delete()

    return redirect('internal:client.index')
