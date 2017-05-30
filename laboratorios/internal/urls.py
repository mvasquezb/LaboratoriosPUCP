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
    # User
    #
    url('^user/$',
        views.user.index,
        name='user.index'),
    url('^user/create$',
        views.user.create,
        name='user.create'),
    url('^user/edit/(?P<pk>\d+)$',
        views.user.edit,
        name='user.edit'),
    url('^user/delete/(?P<pk>\d+)$',
        views.user.delete,
        name='user.delete'),
]
