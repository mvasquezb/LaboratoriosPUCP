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

    #URL de requestStorage
    url('^inventoryOrder/?$',
        views.inventoryOrder.index,
        name='inventoryOrder.index'),
    url('^inventoryOrder/show/(?P<pk>\d+)$',
        views.inventoryOrder.show,
        name='inventoryOrder.show'),
    url('^inventoryOrder/aprobar/(?P<pk>\d+)$',
        views.inventoryOrder.aprobar,
        name='inventoryOrder.aprobar'),
    url('^inventoryOrder/rechazar/(?P<pk>\d+)$',
        views.inventoryOrder.rechazar,
        name='inventoryOrder.rechazar'),
]
