from django.conf.urls import url
from . import views

urlpatterns = [
    #
    # Index
    #
    url('^$',
        views.main.index,
        name='index'),

    #URL de requestStorage
    url('^requestStorage/?$',
        views.requestStorage.index,
        name='requestStorage.index'),
    url('^requestStorage/aprobar/?$',
        views.requestStorage.aprobar,
        name='requestStorage.aprobar'),
    url('^requestStorage/rechazar/?$',
        views.requestStorage.rechazar,
        name='requestStorage.rechazar'),
]
