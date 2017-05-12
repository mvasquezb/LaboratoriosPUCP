from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),
    url('^list_products',
        views.main.lista_productos,
        name='lista_productos'),
]
