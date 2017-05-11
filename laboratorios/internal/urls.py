from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$', views.main.index, name='index'),
    url('^clients/$', views.clients.index, name='index_clients'),
    url('^clients/new$', views.clients.create_new_client, name='clients_create'),
]
