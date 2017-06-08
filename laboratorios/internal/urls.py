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

    
    #
    # ServiceRequest
    #
    url('^servicerequest/create/(?P<pk>\d+)$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/select_client$',
        views.servicerequest.select_client,
        name='servicerequest.select_client'),
   url('^servicerequest/edit/(?P<pk>\d+)$',
        views.servicerequest.edit,
        name='servicerequest.edit'),     
    url('^servicerequest/add_sample/(?P<pk>\d+)$',
        views.servicerequest.add_sample,
        name='servicerequest.add_sample'),         
    url('^servicerequest/create_client$',
        views.servicerequest.create_client,
        name='servicerequest.create_client'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),

]
