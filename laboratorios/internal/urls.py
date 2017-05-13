from django.conf.urls import url
from . import views
##
## Insert reference to __init__.py for each view
##

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
    url('^edit',
        views.main.editar_ventas,
        name='editar_ventas'),
    url(r'^suma/(?P<number_1>[0-9]+)/(?P<number_2>[0-9]+)',
        views.main.sumita,
        name='sumita'),
    url('^products/$',
        views.main.lista_productos,
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
    url('^sales/create$',
        views.sales.create,
        name='sale.create'),
]
