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
    url('^request/create$',
        views.request.create,
        name='request.create'),
    url('^request/store$',
        views.request.store,
        name='request.store'),
    url('^request$',
        views.request.index,
        name='request.index'),
    #
    # Test
    #
    url('^test/create$',
        views.test.create,
        name='test.create'),
    url('^test/store$',
        views.test.store,
        name='test.store'),
    url('^test$',
        views.test.index,
        name='test.index'),
    #
    # Service
    #
    url('^service/index/?$',
        views.service.index,
        name='service.index'),
    url('^service/(?P<pk>\d+)/?$',
        views.service.show,
        name='service.show'),
]
