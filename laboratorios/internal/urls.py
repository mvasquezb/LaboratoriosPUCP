from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^list',
        views.main.lista_ventas,
        name='lista_ventas'),
]
