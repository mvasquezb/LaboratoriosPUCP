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
    url('^test/edit/(?P<pk>\d+)$',
        views.test.edit,
        name='test.edit'),
    url('^test/delete/(?P<pk>\d+)$',
        views.test.edit,
        name='test.delete'),
    #
    #Access
    #
    url('^access$',
        views.access.index,
        name='access.index'),
    url('^access/create$',
        views.access.create,
        name='access.create'),
    url('^access/edit/(?P<pk>\d+)$',
        views.access.edit,
        name='access.edit'),
    url('^access/delete/(?P<pk>\d+)$',
        views.access.delete,
        name='access.delete'),


    #
    #Client
    #
    url('^client/$',
        views.client.index,
        name='client.index'),
    url('^client/create$',
        views.client.create,
        name='client.create'),
    url('^client/edit/(?P<pk>\d+)$',
        views.client.edit,
        name='client.edit'),
    url('^client/delete/(?P<pk>\d+)$',
        views.client.delete,
        name='client.delete'),

]
