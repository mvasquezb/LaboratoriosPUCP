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
    url('^edit',
        views.main.editar_ventas,
        name='editar_ventas'),
    url(r'^suma/(?P<number_1>[0-9]+)/(?P<number_2>[0-9]+)',
        views.main.sumita,
        name='sumita'),
]
