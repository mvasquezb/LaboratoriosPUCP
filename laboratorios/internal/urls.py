from django.conf.urls import url, include

from . import views

#Lugar donde se pone los Url's para el proyecto

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
    url('^essayType/update/(?P<id>\d+)/$',
        views.essayType.update,
        name='essayType.update'),
    #
    #Test Type
    #
    url('^testType/?$',
        views.testType.index,
        name='testType.index'),
    url('^testType/create?$',
        views.testType.create,
        name='testType.create'),
    url('^testType/edit?$',
        views.testType.edit,
        name='testType.edit'),
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
    url('^request/?$',
        views.request.index,
        name='request.index'),
    #
    #Servicio de Agregar una muestra a inventario
    #Por Sergio Cama
    #
    #Se observa los almacenes
    url('^requestStorage/?$',
        views.requestStorage.index,
        name='requestStorage.index'),
    url('^requestStorage/aprobar/?$',
        views.requestStorage.aprobar,
        name='requestStorage.aprobar'),
    url('^requestStorage/rechazar/?$',
        views.requestStorage.rechazar,
        name='requestStorage.rechazar'),

]
