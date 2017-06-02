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
    url('^laboratory/delete/?$',
        views.laboratory.delete,
        name='laboratory.delete'),
    url('^laboratory/edit/(?P<id_lab>\d+)/$',
        views.laboratory.edit,
        name='laboratory.edit'),
    url('^laboratory/assignMonitor/(?P<id>\d+)/$',
        views.laboratory.assignMonitor,
        name='laboratory.assignMonitor'),
    #
    #Assay Type
    #
    url('^essayType/?$',
        views.essayType.index,
        name='essayType.index'),
    url('^essayType/create?$',
        views.essayType.create,
        name='essayType.create'),
    url('^essayType/edit/(?P<id>\d+)/$',
        views.essayType.edit,
        name='essayType.edit'),
    url('^essayType/delete/?$',
        views.essayType.delete,
        name='essayType.delete'),
    #
    #Test Type
    #
    url('^testType/?$',
        views.testType.index,
        name='testType.index'),
    url('^testType/create?$',
        views.testType.create,
        name='testType.create'),
    url('^testType/edit/(?P<id>\d+)/$',
        views.testType.edit,
        name='testType.edit'),
    url('^testType/delete/?$',
        views.testType.delete,
        name='testType.delete'),
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
    url('^request/create$',
        views.request.create,
        name='request.create'),
    url('^request/store$',
        views.request.store,
        name='request.store'),
    url('^request$',
        views.request.index,
        name='request.index'),
]
