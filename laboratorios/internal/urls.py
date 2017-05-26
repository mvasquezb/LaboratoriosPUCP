from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^labs$',
        views.labs.index,
        name='labs.index'),
    url('^labs/create$',
        views.labs.create,
        name='labs.create'),
    url('^labs/list$',
        views.labs.list,
        name='labs.list'),
]
