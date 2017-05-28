from django.conf.urls import url

from . import views



urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^laboratory/?$',
        views.labs.index,
        name='labs.index'),
    url('^laboratory/create/?$',
        views.labs.create,
        name='labs.create'),
    url('^role/$', views.role.role_list,name='roles_list'),
    url('^role/create$', views.role.role_create,name='role_create'),
    url('^role/edit/(?P<pk>\d+)%', views.role.role_update,name='role_edit'),
    url('^role/delete/(?P<pk>\d+)%', views.role.role_delete,name='role_delete'),
    url('^request/create$', views.request.create, name='request.create'),
    url('^request/store$', views.request.store, name='request.store'),
    url('^request$', views.request.index, name='request.index'),
]
