from django.conf.urls import url
from . import views
##
## Insert reference to __init__.py for each view
##

urlpatterns = [
    #
    # Index
    #
    url('^$', views.main.index, name='index'),
    url('^clients/$', views.clients.index, name='client.index'),
    url('^clients/create$', views.clients.create, name='client.create'),
    url('^sales/create$', views.sales.create, name='sale.create'),
]
