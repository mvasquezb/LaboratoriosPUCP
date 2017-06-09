from django.conf.urls import url
from . import views
from django.contrib.auth.views import login, logout_then_login

urlpatterns = [
    #
    # Login
    #
    url(r'^login$',
        login,
        {'template_name' : 'internal/login.html'},
        name='login'),

        url(r'^logout$',
        logout_then_login,
        name='logout'),
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
    #
    # RequestStorage
    #
    url('^inventoryOrder/?$',
        views.inventoryOrder.index,
        name='inventoryOrder.index'),
    url('^inventoryOrder/show/(?P<pk>\d+)$',
        views.inventoryOrder.show,
        name='inventoryOrder.show'),
    url('^inventoryOrder/approve/(?P<pk>\d+)$',
        views.inventoryOrder.approve,
        name='inventoryOrder.approve'),
    url('^inventoryOrder/reject/(?P<pk>\d+)$',
        views.inventoryOrder.reject,
        name='inventoryOrder.reject'),

    #
    # ServiceRequest
    #
    url('^servicerequest/create/(?P<pk>\d+)$',
        views.servicerequest.create,
        name='servicerequest.create'),
    url('^servicerequest/delete/(?P<pk>\d+)$',
        views.servicerequest.delete,
        name='servicerequest.delete'),
    url('^servicerequest/select_client$',
        views.servicerequest.select_client,
        name='servicerequest.select_client'),
   url('^servicerequest/edit/(?P<pk>\d+)$',
        views.servicerequest.edit,
        name='servicerequest.edit'),
    url('^servicerequest/add_sample/(?P<pk>\d+)$',
        views.servicerequest.add_sample,
        name='servicerequest.add_sample'),
    url('^servicerequest/edit_sample/(?P<pk_request>\d+)/(?P<pk_sample>\d+)$',
        views.servicerequest.edit_sample,
        name='servicerequest.edit_sample'),
    url('^servicerequest/delete_sample/(?P<pk_request>\d+)/(?P<pk_sample>\d+)$',
        views.servicerequest.delete_sample,
        name='servicerequest.delete_sample'),
    url('^servicerequest/create_client$',
        views.servicerequest.create_client,
        name='servicerequest.create_client'),
    url('^servicerequest$',
        views.servicerequest.index,
        name='servicerequest.index'),
    url('^servicerequest/(?P<request_id>\d+)/?$',
        views.servicerequest.show,
        name='servicerequest.show'),
    url('^servicerequest/(?P<request_id>\d+)/quotation/?$',
        views.servicerequest.quotation,
        name='servicerequest.quotation'),
    url('^servicerequest/(?P<request_id>\d+)/assign_employee/(?P<sample_id>\d+)/?$',
        views.servicerequest.assign_employee,
        name='servicerequest.assign_employee'),
    url('^servicerequest/view_workload_per_request$',
        views.servicerequest.workload_view_per_request,
        name='servicerequest.workload_view_per_request')
]
