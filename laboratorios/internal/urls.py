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
    # Employee
    #
    url('^employee/$',
        views.employee.index,
        name='employee.index'),
    url('^employee/create$',
        views.employee.create,
        name='employee.create'),
    url('^employee/edit/(?P<pk>\d+)$',
        views.employee.edit,
        name='employee.edit'),
    url('^employee/show/(?P<pk>\d+)$',
        views.employee.show,
        name='employee.show'),
    url('^employee/delete/(?P<pk>\d+)$',
        views.employee.delete,
        name='employee.delete'),
    url('^role/$',
        views.role.index,
        name='role.index'),
    url('^role/show/(?P<pk>\d+)$',
        views.role.show,
        name='role.show'),
    url('^role/create$',
    views.role.create,
    name='role.create'),
    url('^role/edit/(?P<pk>\d+)$',
    views.role.edit,
    name='role.edit'),
        url('^role/delete/(?P<pk>\d+)$',
        views.role.delete,
        name='role.delete'),


]
