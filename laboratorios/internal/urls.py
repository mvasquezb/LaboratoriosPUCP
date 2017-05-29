from django.conf.urls import url

from . import views


urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    #
    # Laboratory
    #
    url('^laboratory/?$',
        views.laboratory.index,
        name='laboratory.index'),
    url('^laboratory/create/?$',
        views.laboratory.create,
        name='laboratory.create'),
    #
    # Role
    #
    url('^role/$',
        views.role.index,
        name='role.index'),
    url('^role/create$',
        views.role.create,
        name='role.create'),
    url('^role/edit/(?P<pk>\d+)$',
        views.role.edit,
        name='role.edit'),
    url('^role/delete/(?P<pk>\d+)$',
        views.role.delete,
        name='role.delete'),
    #
    # ServiceRequest
    #
    url('^servicerequest/create$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/store$',
        views.servicerequest.store,
        name='servicerequest.store'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),
]
