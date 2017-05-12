from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$', views.main.index, name='index'),
    url('^clients/$', views.clients.index, name='client.index'),
    url('^clients/create$', views.clients.create, name='client.create'),
    url ('^products/edit/(?P<id>\d+)', views.products.edit, name="product.edit"),
    url ('^products/update/(?P<id>\d+)', views.products.update, name="product.update"),
]
