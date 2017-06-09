from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator


__all__ = (
    'index',
)


def index(request,
          template='internal/index.html',
          extra_context=None):
    context = {}
    if extra_context is not None:
        context.update(extra_context)
    return render(request, template, context)