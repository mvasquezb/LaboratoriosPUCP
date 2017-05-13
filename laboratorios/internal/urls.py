from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^clients/$',
        views.clients.index,
        name='client.index'),
    url('^clients/create$',
        views.clients.create,
        name='client.create'),
    url('^clients/(?P<client_id>[0-9]+)/edit$',
        views.clients.edit,
        name='client.edit'),
    url('^clients/(?P<client_id>[0-9]+)/update$',
        views.clients.update,
        name='client.update'),
    url('^list',
        views.main.lista_ventas,
        name='lista_ventas'),
    url('^products/$',
        views.products.index,
        name='product.index'),
    url('^products/create$',
        views.products.create,
        name='product.create'),
    url('^products/edit/(?P<id>\d+)',
        views.products.edit,
        name="product.edit"),
    url('^products/update/(?P<id>\d+)',
        views.products.update,
        name="product.update"),
]
