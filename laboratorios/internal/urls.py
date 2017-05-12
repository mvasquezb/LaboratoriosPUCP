from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$', views.main.index, name='index'),
    url('^clients/$', views.clients.index, name='client.index'),
    url('^clients/create$', views.clients.create, name='client.create'),
    url('^clients/(?P<client_id>[0-9]+)/edit$', views.clients.edit, name='client.edit'),
    url('^clients/(?P<client_id>[0-9]+)/update$', views.clients.update, name='client.update'),
]
